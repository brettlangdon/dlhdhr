import base64
import time
from typing import Iterator
import urllib.parse
import re


from lxml import html
import httpx
import m3u8

from dlhdhr import config

from dlhdhr.dlhd.channels import DLHDChannel, get_channels


class DLHDClient:
    CHANNEL_REFRESH = 60 * 60 * 12  # every 12 hours

    _channels: dict[str, DLHDChannel]
    _channels_last_fetch: float = 0
    _base_urls: dict[DLHDChannel, (float, str)]
    _referers: dict[DLHDChannel, str]

    def __init__(self):
        self._channels = {}
        self._base_urls = {}
        self._referers = {}

    async def _log_request(self, request):
        if config.DEBUG:
            print(f"Request event hook: {request.method} {request.url} - Waiting for response")

    async def _log_response(self, response):
        if config.DEBUG:
            request = response.request
            print(f"Response event hook: {request.method} {request.url} - Status {response.status_code}")

    def _get_client(self, referer: str = ""):
        parsed = urllib.parse.urlparse(referer)
        origin = f"{parsed.scheme}://{parsed.netloc}"
        referer = f"{parsed.scheme}://{parsed.netloc}/"

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0",
            "Origin": origin,
            "Referer": referer,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "Sec-GPC": "1",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers",
        }
        return httpx.AsyncClient(
            base_url=config.DLHD_BASE_URL,
            headers=headers,
            max_redirects=2,
            verify=True,
            timeout=8.0,
            event_hooks={"request": [self._log_request], "response": [self._log_response]},
        )

    def get_channels(self) -> Iterator[DLHDChannel]:
        return get_channels()

    def get_channel(self, channel_number: str) -> DLHDChannel | None:
        for channel in self.get_channels():
            if channel.number == channel_number:
                return channel
        return None

    async def get_channel_referer(self, channel: DLHDChannel) -> str:
        if channel not in self._referers:
            base_url = f"https://weblivehdplay.ru/premiumtv/daddyhd.php?id={channel.number}"
            referer = f"https://dlhd.sx/stream/stream-{channel.number}.php"
            async with self._get_client(referer=referer) as client:
                res = await client.get(base_url, follow_redirects=True)
                res.raise_for_status()
                self._referers[channel] = str(res.request.url)
        return self._referers[channel]

    async def get_channel_playlist(self, channel: DLHDChannel) -> m3u8.M3U8:
        base_url = f"https://weblivehdplay.ru/premiumtv/daddyhd.php?id={channel.number}"
        referer = f"https://dlhd.sx/stream/stream-{channel.number}.php"

        async with self._get_client(referer=referer) as client:
            res = await client.get(base_url, follow_redirects=True)
            res.raise_for_status()
            referer = str(res.request.url)

            content = html.fromstring(res.content)
            scripts = content.cssselect(".player_div script")
            index_m3u8_url = None
            for script in scripts:
                urls = re.findall(r"source:'(https://.*?index\.m3u8.*?)'", script.text)
                if urls:
                    index_m3u8_url = urls[0]
                    break
            else:
                raise ValueError("Could not find index m3u8")

        async with self._get_client(referer=referer) as client:
            res = await client.get(index_m3u8_url, follow_redirects=True)
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
        referer = await self.get_channel_referer(channel)

        async with self._get_client(referer=referer) as client:
            res = await client.get(proxy_url)
            res.raise_for_status()

            return res.content

    async def get_channel_base_url(self, channel: DLHDChannel) -> str:
        created, base_url = self._base_urls.get(channel, (None, None))
        if not created or not base_url:
            # This is how we get and populate the base url
            await self.get_channel_playlist(channel)
            return self._base_urls[channel][1]

        if (time.time() - created) > 60:
            await self.get_channel_playlist(channel)
            return self._base_urls[channel][1]

        return base_url

    async def stream_segment(self, channel: DLHDChannel, segment_path: str):
        referer = await self.get_channel_referer(channel)
        base_url = await self.get_channel_base_url(channel)
        segment_url = urllib.parse.urljoin(base_url, segment_path)

        async with self._get_client(referer=referer) as client:
            async with client.stream("GET", segment_url, follow_redirects=True) as res:
                async for chunk in res.aiter_bytes():
                    yield chunk
