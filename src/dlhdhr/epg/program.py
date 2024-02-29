import datetime
from dataclasses import dataclass, field
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
    tags: list[str] = field(default_factory=list)
    subtitle: str | None = None
    thumbnail: str | None = None
    season: int | None = None
    episode: int | None = None
    rating: Rating | None = None
    release_year: str | None = None
    dd_progid: str | None = None

    @property
    def duration_minutes(self) -> int:
        return int((self.end_time - self.start_time).total_seconds() / 60)

    def to_xmltv(self, channel: DLHDChannel) -> Element | None:
        start_time = self.start_time.strftime("%Y%m%d%H%M%S %z")
        end_time = self.end_time.strftime("%Y%m%d%H%M%S %z")

        programme = Element("programme", attrib={"start": start_time, "stop": end_time, "channel": str(channel.number)})
        if self.title:
            SubElement(programme, "title", attrib={"lang": "en"}).text = self.title
        if self.subtitle:
            SubElement(programme, "sub-title", attrib={"lang": "en"}).text = self.subtitle
        else:
            SubElement(programme, "sub-title", attrib={"lang": "en"}).text = self.title
        if self.description:
            SubElement(programme, "desc", attrib={"lang": "en"}).text = self.description

        SubElement(programme, "length", attrib={"units": "minutes"}).text = str(self.duration_minutes)

        if self.release_year:
            SubElement(programme, "date").text = self.release_year

        for tag in self.tags:
            SubElement(programme, "category", attrib={"lang": "en"}).text = tag

        if self.thumbnail:
            SubElement(programme, "icon", attrib={"src": self.thumbnail})

        if self.season and self.episode:
            if self.season and self.episode:
                SubElement(
                    programme, "episode-num", attrib={"system": "xmltv_ns"}
                ).text = f"{self.season}.{self.episode}."
                SubElement(
                    programme, "episode-num", attrib={"system": "onscreen"}
                ).text = f"S{self.season} E{self.episode}"
        if self.dd_progid:
            SubElement(programme, "episode-num", attrib={"system": "dd_progid"}).text = self.dd_progid

        if self.rating:
            rating = SubElement(programme, "rating", attrib={"system": self.rating.system})
            SubElement(rating, "value").text = self.rating.value

        return programme
