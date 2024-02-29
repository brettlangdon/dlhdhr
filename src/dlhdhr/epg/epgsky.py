import datetime
from dataclasses import dataclass, field
import time

import httpx

from dlhdhr import config
from dlhdhr.dlhd.channels import DLHDChannel, get_channels
from dlhdhr.epg.program import Program


@dataclass()
class EPGSky:
    _BASE_URL = "https://awk.epgsky.com/hawk/linear"
    _listings: dict[str, Program] = field(default_factory=dict)
    _last_fetch: float = 0

    def _get_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=self._BASE_URL,
            timeout=5.0,
            verify=True,
            max_redirects=1,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
                "Origin": "https://www.sky.com",
                "Referer": "https://www.sky.com/",
                "Accept": "application/json",
            },
        )

    def _cleanup_listings(self) -> None:
        now = datetime.datetime.now(datetime.UTC)
        cutoff = now - datetime.timedelta(hours=3)

        updated: dict[str, list[Program]] = {}
        for epgsky_id, programs in self._listings.items():
            updated_programs = [p for p in programs if p.end_time > cutoff]
            if updated_programs:
                updated[epgsky_id] = updated_programs
        self._listings = updated

    async def _fetch_listings(self) -> dict[str, list[Program]]:
        listings: dict[str, list[Program]] = {}
        now = datetime.datetime.now(datetime.UTC)
        cutoff = now - datetime.timedelta(hours=3)
        async with self._get_client() as client:
            channels: list[str] = [c.epgsky_id for c in get_channels() if c.epgsky_id]
            date = now.strftime("%Y%m%d")
            for i in range(0, len(channels), 20):
                services = channels[i : i + 20]

                res = await client.get(f"/schedule/{date}/{','.join(services)}")
                res.raise_for_status()

                data = res.json()
                for channel in data["schedule"]:
                    programs = []
                    for event in channel["events"]:
                        start_time = datetime.datetime.fromtimestamp(event["st"], datetime.UTC)
                        end_time = start_time + datetime.timedelta(seconds=event["d"])
                        if end_time < cutoff:
                            continue

                        programs.append(
                            Program(
                                start_time=start_time,
                                end_time=end_time,
                                title=event["t"],
                                subtitle=None,
                                description=event.get("sy") or "",
                                season=event.get("seasonnumber") or None,
                                episode=event.get("episodenumber") or None,
                                tags=[],
                                release_year=None,
                                thumbnail=None,
                                rating=None,
                            )
                        )

                    listings[channel["sid"]] = sorted(programs, key=lambda p: p.start_time)

        return listings

    async def _refresh_listings(self) -> dict[str, list[Program]]:
        self._cleanup_listings()

        now = time.time()
        if self._listings and now - self._last_fetch > config.EPGSKY_REFRESH_DELAY:
            return self._listings

        programs = await self._fetch_listings()
        for code, programs in programs.items():
            if code in self._listings:
                self._listings[code].extend(programs)
            else:
                self._listings[code] = programs
        return self._listings

    async def get_channel_programs(self, channel: DLHDChannel) -> list[Program]:
        if not channel.epgsky_id:
            return []

        await self._refresh_listings()

        if channel.epgsky_id not in self._listings:
            return []

        return self._listings[channel.epgsky_id]
