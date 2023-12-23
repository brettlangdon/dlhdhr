from xml.etree.ElementTree import Element, SubElement, tostring

from dlhdhr.dlhd import DLHDChannel
from dlhdhr.zap2it import Zap2it


async def generate_xmltv(channels: list[DLHDChannel], zap2it: Zap2it) -> bytes:
    tv = Element("tv", attrib={"generator-info-name": "dlhdhr"})

    for channel in channels:
        ch_node = SubElement(tv, "channel", attrib={"id": channel.number})
        SubElement(ch_node, "display-name", attrib={"lang": "en"}).text = channel.name
        SubElement(ch_node, "lcn").text = channel.number

        if not channel.call_sign:
            continue

        z_channel = await zap2it.get_channel(channel.call_sign)

        if not z_channel:
            continue

        if not channel.tvg_id:
            continue

        for event in z_channel.events:
            start_time = event.start_time.strftime("%Y%m%d%H%M%S %z")
            end_time = event.start_time.strftime("%Y%m%d%H%M%S %z")

            programme = SubElement(
                tv, "programme", attrib={"start": start_time, "stop": end_time, "channel": channel.tvg_id}
            )
            if event.program.title:
                SubElement(programme, "title", attrib={"lang": "en"}).text = event.program.title
            if event.program.short_desc:
                SubElement(
                    programme, "desc", attrib={"lang": "en", "desc": event.program.short_desc}
                ).text = event.program.short_desc

            if event.program.release_year:
                SubElement(programme, "date").text = event.program.release_year

            if event.rating:
                rating = SubElement(programme, "rating", attrib={"system": "MPAA"})
                SubElement(rating, "value").text = event.rating

            if event.program.season or event.program.episode:
                e_id = ".".join([event.program.season or "", event.program.episode or "", ""])
                SubElement(programme, "episode-num", attrib={"system": "xmltv_ns"}).text = e_id

            if event.thumbnail:
                SubElement(programme, "icon", attrib={"src": event.thumbnail})

            for tag in event.tags:
                SubElement(programme, "category", attrib={"lang": "en"}).text = tag
    return tostring(tv)