import asyncio

from dlhdhr import config


class FFMpegNotStartedError(Exception):
    pass


class FFMpegProcess:
    _ffmpeg_command: str
    _started: bool = False
    _process: asyncio.subprocess.Process | None = None

    def __init__(self, playlist_url: str):
        log_level = "quiet"
        if config.DEBUG:
            log_level = "debug"

        self._ffmpeg_command = " ".join(
            [
                "ffmpeg",
                "-i",
                f'"{playlist_url}"',
                "-vcodec",
                "copy",
                "-acodec",
                "copy",
                "-crf",
                "18",
                "-preset",
                "ulstrafast",
                "-f",
                "mpegts",
                "-loglevel",
                log_level,
                "pipe:1",
            ]
        )

    @property
    def started(self) -> bool:
        return self._process is not None

    def __aiter__(self) -> "FFMpegProcess":
        return self

    async def __anext__(self):
        if not self.started:
            raise FFMpegNotStartedError()

        if not self._process.stdout:
            raise FFMpegNotStartedError()

        b = await self._process.stdout.read(512)
        if not b:
            raise StopAsyncIteration
        return b

    async def _start(self) -> None:
        if not self._process:
            stderr = asyncio.subprocess.DEVNULL
            if config.DEBUG:
                # When debugging let ffmpeg write to normal stderr
                # do we see the logs in the application stderr
                stderr = None

            self._process = await asyncio.subprocess.create_subprocess_shell(
                self._ffmpeg_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=stderr,
            )

    def _stop(self) -> None:
        if self._process:
            self._process.kill()

    async def __aenter__(self) -> "FFMpegProcess":
        await self._start()
        return self

    async def __aexit__(self, _exc_type, _exc_value, _traceback) -> None:
        self._stop()

    def __repr__(self) -> str:
        return f"FFMpegProcess<started={self.started}, command={self._ffmpeg_command:!r}>"
