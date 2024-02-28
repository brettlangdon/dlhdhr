import datetime
from dataclasses import dataclass
from xml.etree.ElementTree import Element, SubElement

from dlhdhr.dlhd import DLHDChannel


@dataclass(frozen=True)
class Rating:
    system: str
    value: str


@dataclass(frozen=True)
class Program:
    start_time: datetime.datetime
    end_time: datetime.datetime
    title: str
    description: str
    tags: list[str]
    subtitle: str | None
    thumbnail: str | None
    season: int | None
    episode: int | None
    rating: Rating | None
    release_year: str | None

    def to_xmltv(self, channel: DLHDChannel) -> Element | None:
        if not channel.xmltv_id:
            return None

        start_time = self.start_time.strftime("%Y%m%d%H%M%S %z")
        end_time = self.start_time.strftime("%Y%m%d%H%M%S %z")

        programme = Element("programme", attrib={"start": start_time, "stop": end_time, "channel": channel.xmltv_id})
        if self.title:
            SubElement(programme, "title", attrib={"lang": "en"}).text = self.title
        if self.subtitle:
            SubElement(programme, "sub-title", attrib={"lang": "en"}).text = self.subtitle
        if self.description:
            SubElement(programme, "desc", attrib={"lang": "en"}).text = self.description

        if self.release_year:
            SubElement(programme, "date").text = self.release_year

        for tag in self.tags:
            SubElement(programme, "category", attrib={"lang": "en"}).text = tag

        if self.thumbnail:
            SubElement(programme, "icon", attrib={"src": self.thumbnail})

        if self.season or self.episode:
            season_id = self.season or ""
            episode_id = self.episode or ""
            SubElement(programme, "episode-num", attrib={"system": "xmltv_ns"}).text = f"{season_id}.{episode_id}."
            if self.season and self.episode:
                SubElement(
                    programme, "episode-num", attrib={"system": "onscreen"}
                ).text = f"S{self.season} E{self.episode}"

        if self.rating:
            rating = SubElement(programme, "rating", attrib={"system": self.rating.system})
            SubElement(rating, "value").text = self.rating.value

        return programme
