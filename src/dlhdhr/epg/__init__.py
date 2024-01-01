from dataclasses import dataclass, field
from typing import Iterable
from xml.etree.ElementTree import Element, tostring


from dlhdhr.dlhd import DLHDChannel
from dlhdhr.epg.zap2it import Zap2it
from dlhdhr.epg.program import Program


@dataclass()
class EPG:
    zap2it: Zap2it = field(default_factory=Zap2it)

    async def get_channel_programs(self, channel: DLHDChannel) -> list[Program]:
        if channel.country_code == "us":
            return await self.zap2it.get_channel_programs(channel)
        elif channel.country_code == "uk":
            # TODO: TV24? TV Guide?
            return []

        return []

    async def generate_xmltv(self, channels: Iterable[DLHDChannel]) -> bytes:
        tv = Element("tv", attrib={"generator-info-name": "dlhdhr"})

        channels = [c for c in channels if c.xmltv_id]

        for channel in channels:
            tv.append(channel.to_xmltv())

        for channel in channels:
            programs = await self.get_channel_programs(channel)

            # Note: The order of the elements in the <programme /> matters
            # title, desc, date, category, icon, episode-num, rating
            for program in programs:
                node = program.to_xmltv(channel)
                if node:
                    tv.append(node)
        return tostring(tv)
