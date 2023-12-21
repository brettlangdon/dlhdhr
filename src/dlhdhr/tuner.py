import asyncio
import time
import weakref

from dlhdhr.dlhd import DLHDChannel
from dlhdhr.ffmpeg import FFMpegProcess
from m3u8.httpclient import urllib

from dlhdhr import config


class Tuner:
    TUNER_TIMEOUT: int = 20

    _channel: DLHDChannel
    _ffmpeg_process: FFMpegProcess
    _listeners: weakref.WeakSet["Tuner.Listener"]
    _stream_task: asyncio.Task | None = None

    class Listener:
        _queue: asyncio.Queue
        _stopped: bool = False

        def __init__(self):
            self._queue = asyncio.Queue()

        def write(self, chunk: bytes | None) -> None:
            if not self._stopped:
                self._queue.put_nowait(chunk)

        def _stop(self) -> None:
            self._stopped = True
            self._queue.empty()

        def __aiter__(self) -> "Tuner.Listener":
            return self

        async def __anext__(self):
            if self._stopped:
                raise StopAsyncIteration()
            chunk = await self._queue.get()
            if not chunk:
                raise StopAsyncIteration()

            return chunk

    def __init__(self, channel: DLHDChannel):
        # We can use the binding ip/port here since it should all local traffic
        base_url = f"http://{config.HOST}:{config.PORT}/"
        absolute_url = urllib.parse.urljoin(base_url, channel.playlist_m3u8)

        self._channel = channel
        self._ffmpeg_process = FFMpegProcess(absolute_url)
        self._listeners = weakref.WeakSet()

    async def _stream(self) -> None:
        try:
            stream_timeout: float | None = None
            async with self._ffmpeg_process:
                async for chunk in self._ffmpeg_process:
                    # If there are no listeners, stream for up to 20 more seconds
                    # to see if a listener comes back, if not, then stop the stream
                    if not self._listeners:
                        if not stream_timeout:
                            stream_timeout = time.time()
                        elif time.time() - stream_timeout > Tuner.TUNER_TIMEOUT:
                            break
                        else:
                            continue
                    elif stream_timeout:
                        stream_timeout = None

                    for listener in self._listeners:
                        listener.write(chunk)
                        # Make sure we don't hold any hard references to
                        # these weakrefs
                        del listener
        finally:
            self._stop()

    async def _start(self) -> None:
        if self._stream_task:
            return

        self._stream_task = asyncio.create_task(self._stream())

    def _stop(self) -> None:
        if self._stream_task:
            self._stream_task.cancel()
            self._stream_task = None

        self._ffmpeg_process._stop()
        for listener in self._listeners:
            listener._stop()
        self._listeners.clear()

    async def get_listener(self) -> "Tuner.Listener":
        # Make sure to add listener before starting the stream
        listener = self.Listener()
        self._listeners.add(listener)

        if not self._ffmpeg_process.started:
            await self._start()

        return listener

    @property
    def channel(self) -> DLHDChannel:
        return self._channel

    @property
    def has_listeners(self) -> bool:
        return bool(self.num_listeners)

    @property
    def num_listeners(self) -> int:
        return len(self._listeners)

    def __repr__(self) -> str:
        return f"Tuner<channel={self.channel}, num_listeners={self.num_listeners}>"


class NoAvailableTunersError(Exception):
    pass


class TunerNotFoundError(Exception):
    pass


class TunerManager:
    _max_tuners: int
    _tuners: weakref.WeakValueDictionary[DLHDChannel, Tuner]

    def __init__(self, max_tuners: int = 2) -> None:
        self._max_tuners = max_tuners
        self._tuners = weakref.WeakValueDictionary()

    def __repr__(self) -> str:
        return f"TunerManager<num_tuners={self._max_tuners}, tuners={self._tuners}>"

    @property
    def max_tuners(self) -> int:
        return self._max_tuners

    @property
    def available_tuners(self) -> int:
        return self.max_tuners - len(self._tuners)

    @property
    def total_available_listeners(self) -> int:
        # We can accept more than 1 connection per-tuner
        # So we want to report the total number of listeners + number of available tuners (or 1)
        # This means we might actually tell the client that we have
        # more tuners that we can actually allocate, but we also want
        # to be sure we tell them to try to connect in case they
        # want to stream an already tuned channel
        total_listeners = sum(tuner.num_listeners for tuner in self._tuners.values())

        if not total_listeners:
            return self.max_tuners

        return total_listeners + max(1, self.available_tuners)

    def claim_tuner(self, channel: DLHDChannel) -> Tuner:
        # Cleanup any silent tuners first
        for tuner in list(self._tuners.values()):
            if not tuner.has_listeners:
                tuner._stop()
                del self._tuners[tuner.channel]

        if len(self._tuners) >= self._max_tuners:
            raise NoAvailableTunersError()

        if channel in self._tuners:
            return self._tuners[channel]

        tuner = Tuner(channel)
        self._tuners[channel] = tuner
        return tuner
