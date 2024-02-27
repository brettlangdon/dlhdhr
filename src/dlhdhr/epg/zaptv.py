import datetime
from dataclasses import dataclass, field
import time

import httpx

from dlhdhr import config
from dlhdhr.dlhd.channels import DLHDChannel
from dlhdhr.epg.program import Program
from dlhdhr.epg.program import Rating


@dataclass()
class ZapTV:
    _BASE_URL = "https://www.zaptv.co.uk/api/"
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
                "Referer": "https://www.zaptv.co.uk/",
                "Accept": "application/json",
            },
        )

    def _cleanup_listings(self) -> None:
        now = datetime.datetime.now(datetime.UTC)

        updated: dict[str, list[Program]] = {}
        for call_sign, programs in self._listings.items():
            updated_programs = [p for p in programs if p.end_time > now]
            if updated_programs:
                updated[call_sign] = updated_programs
        self._listings = updated

    async def _fetch_listings(self) -> dict[str, list[Program]]:
        listings: dict[str, list[Program]] = {}
        now = datetime.datetime.now(datetime.UTC)
        async with self._get_client() as client:
            channels = set()
            events = {}

            # TODO: Can we fetch tomorrows data as well?
            res = await client.get(f"/schedules/today")
            res.raise_for_status()

            data = res.json()
            for d in data:
                channel = d["channel"]
                code = channel["code"]
                channels.add(code)

                if code not in events:
                    events[code] = {}

                for broadcast in d["broadcasts"]:
                    events[code][broadcast["uid"]] = broadcast

            for code in channels:
                programs = []
                for evt_data in events[code].values():
                    end_time = datetime.datetime.fromisoformat(evt_data["endsAt"])
                    if end_time < now:
                        continue

                    ep_data = evt_data["metadata"].get("episode") or {}
                    season = ep_data.get("season") or None
                    if season is not None:
                        season = str(season)
                    episode = ep_data.get("number") or None
                    if episode is not None:
                        episode = str(episode)

                    release_year = evt_data["metadata"].get("year")
                    if release_year is not None:
                        release_year = str(release_year)

                    programs.append(
                        Program(
                            start_time=datetime.datetime.fromisoformat(evt_data["startsAt"]),
                            end_time=end_time,
                            title=evt_data["title"],
                            description="",
                            season=season,
                            episode=episode,
                            tags=[],
                            release_year=release_year,
                            thumbnail=evt_data["image"] or None,
                            rating=None,
                        )
                    )

                listings[code] = sorted(programs, key=lambda p: p.start_time, reverse=True)

        return listings

    async def _refresh_listings(self) -> dict[str, list[Program]]:
        self._cleanup_listings()

        now = time.time()
        if self._listings and now - self._last_fetch > config.ZAPTV_REFRESH_DELAY:
            return self._listings

        programs = await self._fetch_listings()
        for code, programs in programs.items():
            if code in self._listings:
                self._listings[code].extend(programs)
            else:
                self._listings[code] = programs
        return self._listings

    async def get_channel_programs(self, channel: DLHDChannel) -> list[Program]:
        if not channel.call_sign:
            return []

        await self._refresh_listings()

        if channel.call_sign not in self._listings:
            return []

        return self._listings[channel.call_sign]
