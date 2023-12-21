from dataclasses import dataclass
import time
import urllib.parse

import lxml.etree
import httpx
import m3u8

from dlhdhr import config

from dlhdhr.tvg_id import get_tvg_id


@dataclass(frozen=True)
class DLHDChannel:
    number: str
    name: str

    @property
    def tvg_id(self) -> str | None:
        return get_tvg_id(self.number)

    @property
    def playlist_m3u8(self) -> str:
        return f"/channel/{self.number}/playlist.m3u8"

    @property
    def channel_proxy(self) -> str:
        return f"/channel/{self.number}"


class DLHDClient:
    CHANNEL_REFRESH = 60 * 60 * 12  # every 12 hours

    _channels: dict[str, DLHDChannel]
    _channels_last_fetch: float = 0
    _base_urls: dict[DLHDChannel, (float, str)]

    def __init__(self):
        self._channels = {}
        self._base_urls = {}

    def _get_client(self, referer: str = ""):
        headers = {
            "User-Agent": "",
            "Referer": referer,
        }
        return httpx.AsyncClient(
            base_url=config.DLHD_BASE_URL,
            headers=headers,
            max_redirects=2,
            verify=True,
            timeout=1.0,
        )

    async def _refresh_channels(self):
        now = time.time()
        if self._channels and now - self._channels_last_fetch < DLHDClient.CHANNEL_REFRESH:
            return

        self._channels_last_fetch = time.time()

        channels: dict[str, DLHDChannel] = {}
        async with self._get_client() as client:
            res = await client.get("/24-7-channels.php")
            res.raise_for_status()

            root = lxml.etree.HTML(res.content)
            for channel_link in root.cssselect(".grid-item a"):
                href: str = channel_link.get("href")
                if not href:
                    continue

                channel_number, _, _ = href.split("-")[1].partition(".")
                channel_number.strip().lower()

                # Skip any not explicitly defined in the allow list
                if config.CHANNEL_ALLOW is not None:
                    if channel_number not in config.CHANNEL_ALLOW:
                        continue

                # Skip any that are explicitly defined in the deny list
                if config.CHANNEL_EXCLUDE is not None:
                    if channel_number in config.CHANNEL_EXCLUDE:
                        cotninue

                channels[channel_number] = DLHDChannel(
                    number=channel_number, name=channel_link.cssselect("strong")[0].text.strip()
                )

        self._channels = channels

    async def get_channels(self) -> list[DLHDChannel]:
        await self._refresh_channels()
        return list(self._channels.values())

    async def get_channel(self, channel_number: str) -> DLHDChannel | None:
        await self._refresh_channels()
        return self._channels.get(channel_number)

    async def get_channel_playlist(self, channel: DLHDChannel) -> m3u8.M3U8:
        index_m3u8 = config.DLHD_INDEX_M3U8_PATTERN.format(channel=channel)

        referer = f"https://weblivehdplay.ru/premiumtv/daddyhd.php?id={channel.number}"
        async with self._get_client(referer=referer) as client:
            res = await client.get(index_m3u8, follow_redirects=True)
            res.raise_for_status()

            playlist = m3u8.loads(res.content.decode())

            # We only expect a single playlist right now
            mono_url = urllib.parse.urljoin(str(res.request.url), playlist.playlists[0].uri)

            res = await client.get(mono_url)
            res.raise_for_status()

            mono_playlist = m3u8.loads(res.content.decode())
            self._base_urls[channel] = (time.time(), mono_url)

        return mono_playlist

    async def get_channel_base_url(self, channel: DLHDChannel) -> str:
        created, base_url = self._base_urls.get(channel, (None, None))
        if not created or not base_url:
            # This is how we get and populate the base url
            await self.get_channel_playlist(channel)
            return self._base_urls[channel][0]

        if (time.time() - created) > 60:
            await self.get_channel_playlist(channel)
            return self._base_urls[channel][0]

        return base_url

    async def stream_segment(self, channel: DLHDChannel, segment_path: str):
        base_url = await self.get_channel_base_url(channel)
        segment_url = urllib.parse.urljoin(base_url, segment_path)

        async with self._get_client(referer=base_url) as client:
            async with client.stream("GET", segment_url, follow_redirects=True) as res:
                async for chunk in res.aiter_bytes():
                    yield chunk
