import datetime
from dataclasses import dataclass, field
import time

import httpx

from dlhdhr import config
from dlhdhr.dlhd.channels import DLHDChannel
from dlhdhr.epg.program import Program
from dlhdhr.epg.program import Rating


@dataclass()
class Zap2it:
    _BASE_URL = "https://tvlistings.zap2it.com/api/"
    _listings: dict[str, Program] = field(default_factory=dict)
    _last_fetch: float = 0

    def _get_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=self._BASE_URL,
            timeout=2.0,
            verify=True,
            max_redirects=1,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
                "Referer": "https://tvlistings.zap2it.com/?aid=gapzap",
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

    async def _fetch_listings(self, lineup_id: str, headend_id: str, postal_code: str) -> dict[str, list[Program]]:
        params = {
            "lineupId": lineup_id,
            "timespan": "6",
            "headendId": headend_id,
            "country": "USA",
            "timezone": "",
            "device": "X",
            "postalCode": postal_code,
            "isOverride": "true",
            "time": str(int(time.time())),
            "pref": "16,256",
            "userId": "-",
            "aid": "gapzap",
            "languagecode": "en-us",
        }

        listings: dict[str, list[Program]] = {}
        now = datetime.datetime.now(datetime.UTC)
        async with self._get_client() as client:
            channels = set()
            events = {}

            # Fetch up to 18 hours into the future
            for i in range(3):
                params["time"] = str(int(time.time()) + (21600 * i))
                res = await client.get("/grid", params=params)
                res.raise_for_status()

                data = res.json()
                for ch_data in data["channels"]:
                    call_sign = ch_data["callSign"]
                    channels.add(call_sign)
                    if call_sign not in events:
                        events[call_sign] = {}

                    for evt in ch_data["events"]:
                        key = (evt["startTime"], evt["endTime"])
                        if key not in events[call_sign]:
                            events[call_sign][key] = evt

            for call_sign in channels:
                programs = []
                for evt_data in events[call_sign].values():
                    end_time = datetime.datetime.fromisoformat(evt_data["endTime"])
                    if end_time < now:
                        continue

                    rating = None
                    if evt_data["rating"]:
                        rating = Rating(system="MPAA", value=evt_data["rating"])

                    programs.append(
                        Program(
                            start_time=datetime.datetime.fromisoformat(evt_data["startTime"]),
                            end_time=end_time,
                            title=evt_data["program"]["title"],
                            description=evt_data["program"]["shortDesc"],
                            season=evt_data["program"]["season"],
                            episode=evt_data["program"]["episode"],
                            tags=evt_data["tags"],
                            release_year=evt_data["program"]["releaseYear"],
                            thumbnail=f"https://zap2it.tmsimg.com/assets/{evt_data['thumbnail']}.jpg?w=165",
                            rating=rating,
                        )
                    )

                listings[call_sign] = sorted(programs, key=lambda p: p.start_time)

        return listings

    async def _refresh_listings(self) -> dict[str, list[Program]]:
        self._cleanup_listings()

        now = time.time()
        if self._listings and now - self._last_fetch > config.ZAP2IT_REFRESH_DELAY:
            return self._listings

        east_coast_programs = await self._fetch_listings(
            lineup_id="USA-NY31519-DEFAULT", headend_id="NY31519", postal_code="10001"
        )
        for call_sign, programs in east_coast_programs.items():
            if call_sign in self._listings:
                self._listings[call_sign].extend(programs)
            else:
                self._listings[call_sign] = programs

        west_coast_programs = await self._fetch_listings(
            lineup_id="USA-CA66511-DEFAULT", headend_id="CA66511", postal_code="90001"
        )
        for call_sign, programs in west_coast_programs.items():
            if call_sign in self._listings:
                self._listings[call_sign].extend(programs)
            else:
                self._listings[call_sign] = programs
        return self._listings

    async def get_channel_programs(self, channel: DLHDChannel) -> list[Program]:
        if not channel.call_sign:
            return []

        await self._refresh_listings()

        if channel.call_sign not in self._listings:
            return []

        return self._listings[channel.call_sign]
