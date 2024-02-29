from dataclasses import dataclass, field
from typing import Iterable
from xml.etree.ElementTree import Element, tostring


from dlhdhr.dlhd import DLHDChannel
from dlhdhr.epg.zap2it import Zap2it
from dlhdhr.epg.program import Program
from dlhdhr.epg.zaptv import ZapTV
from dlhdhr.epg.epgsky import EPGSky


@dataclass()
class EPG:
    epgsky: EPGSky = field(default_factory=EPGSky)
    zap2it: Zap2it = field(default_factory=Zap2it)
    zaptv: ZapTV = field(default_factory=ZapTV)

    async def get_channel_programs(self, channel: DLHDChannel) -> list[Program]:
        if channel.country_code == "us":
            return await self.zap2it.get_channel_programs(channel)
        elif channel.country_code == "uk":
            if channel.epgsky_id:
                return await self.epgsky.get_channel_programs(channel)
            return await self.zaptv.get_channel_programs(channel)

        return []

    async def get_channel_icon_from_epg(self, channel: DLHDChannel) -> str | None:
        if channel.country_code == "uk":
            if channel.epgsky_id:
                return f"https://d2n0069hmnqmmx.cloudfront.net/epgdata/1.0/newchanlogos/80/35/skychb{channel.epgsky_id}.png"
        return None

    async def generate_xmltv(self, channels: Iterable[DLHDChannel]) -> bytes:
        tv = Element("tv", attrib={"generator-info-name": "dlhdhr"})

        channels = [c for c in channels if c.xmltv_id]

        for channel in channels:
            tv.append(channel.to_xmltv(thumbnail=await self.get_channel_icon_from_epg(channel)))

            programs = await self.get_channel_programs(channel)

            # Note: The order of the elements in the <programme /> matters
            # title, desc, date, category, icon, episode-num, rating
            for program in programs:
                node = program.to_xmltv(channel)
                if node:
                    tv.append(node)
        return tostring(tv)
