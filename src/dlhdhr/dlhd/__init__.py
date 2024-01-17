import base64
import time
from typing import Iterator
import urllib.parse

import httpx
import m3u8

from dlhdhr import config

from dlhdhr.dlhd.channels import DLHDChannel, get_channels


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
            timeout=8.0,
        )

    def get_channels(self) -> Iterator[DLHDChannel]:
        return get_channels()

    def get_channel(self, channel_number: str) -> DLHDChannel | None:
        for channel in self.get_channels():
            if channel.number == channel_number:
                return channel
        return None

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

            new_keys = []
            for key in mono_playlist.keys:
                if not key:
                    continue

                uri = str(key.absolute_uri or key.uri)
                if not uri:
                    continue

                proxy_uri = base64.urlsafe_b64encode(uri.encode())
                new_key = m3u8.Key(
                    method=key.method,
                    base_uri=None,
                    uri=f"/channel/{channel.number}/key/{proxy_uri.decode()}",
                    iv=key.iv,
                    keyformat=key.keyformat,
                    keyformatversions=key.keyformatversions,
                    **key._extra_params,
                )
                new_keys.append(new_key)

                for segment in mono_playlist.segments:
                    if segment.key == key:
                        segment.key = new_key

            mono_playlist.keys = new_keys
            self._base_urls[channel] = (time.time(), mono_url)

        return mono_playlist

    async def get_channel_key(self, channel: DLHDChannel, proxy_url: str) -> bytes:
        base_url = await self.get_channel_base_url(channel)

        async with self._get_client(referer=base_url) as client:
            res = await client.get(proxy_url)
            res.raise_for_status()

            return res.content

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
