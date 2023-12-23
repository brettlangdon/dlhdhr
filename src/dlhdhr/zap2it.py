import datetime
from dataclasses import dataclass, field
import time

import httpx

from dlhdhr import config


# Mapping of DLHD channel number to zap2it call sign
_MAPPING = dict(
    [
        ("44", "ESPN"),
        ("45", "ESPN2"),
        ("66", "TUDN"),
        ("295", "TOON"),
        ("298", "FXX"),
        ("301", "FREEFRM"),
        ("303", "AMC"),
        ("305", "BBCA"),
        ("306", "BET"),
        ("307", "BRAVO"),
        ("309", "CNBC"),
        ("310", "COMEDY"),
        ("312", "DISN"),
        ("316", "ESPNU"),
        ("317", "FX"),
        ("319", "GSN"),
        ("321", "HBO"),
        ("325", "ION"),
        ("326", "LIFE"),
        ("327", "MSNBC"),
        ("329", "NICJR"),
        ("330", "NIK"),
        ("331", "OWN"),
        ("333", "SHOW"),
        ("334", "PAR"),
        ("335", "STARZ"),
        ("336", "TBS"),
        ("337", "TLC"),
        ("338", "TNT"),
        ("339", "TOON"),
        ("340", "TRAV"),
        ("343", "USA"),
        ("344", "VH1"),
        ("345", "CNN"),
        ("371", "MTV"),
        ("373", "SYFY"),
        ("381", "FXM"),
        ("382", "HGTV"),
        ("647", "CMTV"),
        ("651", "DEST"),
        ("658", "SUNDANC"),
        ("665", "FYISD"),
        ("689", "HBO2"),
        ("691", "HBOF"),
        ("693", "HBOSIG"),
        ("697", "COOK"),
        ("745", "NGC"),
        ("766", "ABC"),
    ]
)


def get_channel_call_sign(channel_number: str) -> str | None:
    return _MAPPING.get(channel_number)


class Zap2it:
    _BASE_URL = "https://tvlistings.zap2it.com/api/"
    _listings: dict[str, "Zap2it.Channel"]
    _last_fetch: float = 0

    @dataclass
    class Program:
        title: str
        id: str
        short_desc: str
        season: str | None
        release_year: str | None
        episode: str | None
        episode_title: str | None
        series_id: str | None

    @dataclass
    class Event:
        duration: int
        start_time: datetime.datetime
        end_time: datetime.datetime
        thumbnail: str
        series_id: str
        rating: str
        tags: list[str]
        program: "Zap2it.Program"

    @dataclass
    class Channel:
        call_sign: str
        name: str
        number: str
        id: str
        thumbnail: str
        events: list["Zap2it.Event"] = field(default_factory=list)

    def __init__(self):
        self._listings = {}

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

        updated: dict[str, "Zap2it.Channel"] = {}
        for channel in self._listings.values():
            channel.events = [evt for evt in channel.events if evt.end_time > now]
            if channel.events:
                updated[channel.call_sign] = channel
        self._listings = updated

    async def _refresh_listings(self) -> list["Zap2it.Channel"]:
        self._cleanup_listings()

        now = time.time()
        if self._listings and now - self._last_fetch > config.ZAP2IT_REFRESH_DELAY:
            return list(self._listings.values())

        params = {
            "lineupId": config.ZAP2IT_LINEUP_ID,
            "timespan": "6",
            "headendId": config.ZAP2IT_HEADEND_ID,
            "country": "USA",
            "timezone": "",
            "device": "X",
            "postalCode": config.ZAP2IT_POSTAL_CODE,
            "isOverride": "true",
            "time": str(int(time.time())),
            "pref": "16,256",
            "userId": "-",
            "aid": "gapzap",
            "languagecode": "en-us",
        }

        now = datetime.datetime.now(datetime.UTC)
        async with self._get_client() as client:
            res = await client.get("/grid", params=params)
            res.raise_for_status()

            data = res.json()

            for ch_data in data["channels"]:
                call_sign = ch_data["callSign"]
                if call_sign in self._listings:
                    channel = self._listings[call_sign]
                else:
                    channel = self.Channel(
                        call_sign=call_sign,
                        name=ch_data["affiliateName"],
                        number=ch_data["channelNo"],
                        id=ch_data["id"],
                        thumbnail=ch_data["thumbnail"],
                    )
                    self._listings[call_sign] = channel

                for evt_data in ch_data["events"]:
                    end_time = datetime.datetime.fromisoformat(evt_data["endTime"])
                    if end_time < now:
                        continue

                    event = self.Event(
                        duration=evt_data["duration"],
                        rating=evt_data["rating"],
                        tags=evt_data["tags"],
                        thumbnail=f"//zap2it.tmsimg.com/assets/{evt_data['thumbnail']}.jpg?w=165",
                        series_id=evt_data["seriesId"],
                        start_time=datetime.datetime.fromisoformat(evt_data["startTime"]),
                        end_time=end_time,
                        program=self.Program(
                            title=evt_data["program"]["title"],
                            id=evt_data["program"]["id"],
                            short_desc=evt_data["program"]["shortDesc"],
                            season=evt_data["program"]["season"],
                            release_year=evt_data["program"]["releaseYear"],
                            episode=evt_data["program"]["episode"],
                            episode_title=evt_data["program"]["episodeTitle"],
                            series_id=evt_data["program"]["seriesId"],
                        ),
                    )
                    channel.events.append(event)

        return list(self._listings.values())

    async def get_channel(self, call_sign: str) -> Channel | None:
        await self._refresh_listings()

        return self._listings.get(call_sign)