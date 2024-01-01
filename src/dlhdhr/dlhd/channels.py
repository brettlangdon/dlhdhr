from collections.abc import Generator
from dataclasses import dataclass
from xml.etree.ElementTree import Element, SubElement
from typing import Iterator

from dlhdhr import config


@dataclass(frozen=False)
class DLHDChannel:
    number: str
    name: str
    country_code: str
    xmltv_id: str
    call_sign: str

    @property
    def playlist_m3u8(self) -> str:
        return f"/channel/{self.number}/playlist.m3u8"

    @property
    def channel_proxy(self) -> str:
        return f"/channel/{self.number}"

    def to_xmltv(self) -> Element:
        node = Element("channel", attrib={"id": self.xmltv_id})
        SubElement(node, "display-name", attrib={"lang": "en"}).text = self.name
        SubElement(node, "lcn").text = self.number
        return node


_CHANNELS = [
    DLHDChannel(number="31", name="TNT Sports 1 UK", country_code="uk", xmltv_id="TNTSport1.uk", call_sign=""),
    DLHDChannel(number="32", name="TNT Sports 2 UK", country_code="uk", xmltv_id="TNTSport2.uk", call_sign=""),
    DLHDChannel(number="33", name="TNT Sports 3 UK", country_code="uk", xmltv_id="TNTSport3.uk", call_sign=""),
    DLHDChannel(number="34", name="TNT Sports 4 UK", country_code="uk", xmltv_id="TNTSport4.uk", call_sign=""),
    DLHDChannel(
        number="35", name="Sky Sports Football UK", country_code="uk", xmltv_id="SkySportsFootball.uk", call_sign=""
    ),
    DLHDChannel(number="36", name="Sky Sports Arena UK", country_code="uk", xmltv_id="SkySportsArena.uk", call_sign=""),
    DLHDChannel(
        number="37", name="Sky Sports Action UK", country_code="uk", xmltv_id="SkySportsAction.uk", call_sign=""
    ),
    DLHDChannel(
        number="38", name="Sky Sports Main Event", country_code="uk", xmltv_id="SkySportsMainEvent.uk", call_sign=""
    ),
    DLHDChannel(number="39", name="Fox Sports 1 USA", country_code="us", xmltv_id="FoxSports1.us", call_sign=""),
    DLHDChannel(number="40", name="Tennis Channel", country_code="us", xmltv_id="TennisChannel.us", call_sign="TENNIS"),
    DLHDChannel(number="41", name="EuroSport 1 UK", country_code="uk", xmltv_id="Eurosport1.uk", call_sign=""),
    DLHDChannel(number="42", name="EuroSport 2 UK", country_code="uk", xmltv_id="Eurosport2.uk", call_sign=""),
    DLHDChannel(number="43", name="DAZN LaLiga 2", country_code="es", xmltv_id="DaznLaLiga2.es", call_sign=""),
    DLHDChannel(number="44", name="ESPN USA", country_code="us", xmltv_id="ESPN.us", call_sign="ESPN"),
    DLHDChannel(number="45", name="ESPN2 USA", country_code="us", xmltv_id="ESPN2.us", call_sign="ESPN2"),
    DLHDChannel(number="46", name="beIN Sports MENA English 3", country_code="qa", xmltv_id="", call_sign=""),
    DLHDChannel(number="47", name="Polsat Sport Poland", country_code="pl", xmltv_id="PolsatSport.pl", call_sign=""),
    DLHDChannel(number="48", name="Canal+ Sport Poland", country_code="pl", xmltv_id="CanalPlusSport.pl", call_sign=""),
    DLHDChannel(number="49", name="Sport TV1 Portugal", country_code="pt", xmltv_id="SportTV1.pt", call_sign=""),
    DLHDChannel(
        number="50", name="Polsat Sport Extra Poland", country_code="pl", xmltv_id="PolsatSportExtra.pl", call_sign=""
    ),
    DLHDChannel(number="51", name="ABC USA", country_code="us", xmltv_id="", call_sign="WABC"),
    DLHDChannel(number="52", name="CBS USA", country_code="us", xmltv_id="", call_sign="WCBS"),
    DLHDChannel(number="53", name="NBC USA", country_code="us", xmltv_id="", call_sign="WNBC"),
    DLHDChannel(number="54", name="FOX USA", country_code="us", xmltv_id="", call_sign="WNYW"),
    DLHDChannel(
        number="56", name="Supersport Football", country_code="za", xmltv_id="SuperSportFootball.za", call_sign=""
    ),
    DLHDChannel(number="57", name="EuroSport 1 Poland", country_code="pl", xmltv_id="", call_sign=""),
    DLHDChannel(number="58", name="EuroSport 2 Poland", country_code="pl", xmltv_id="Eurosport2.pl", call_sign=""),
    DLHDChannel(number="60", name="Sky Sports F1 UK", country_code="uk", xmltv_id="SkySportsF1.uk", call_sign=""),
    DLHDChannel(number="61", name="beIN Sports MENA English 1", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="62", name="beIN SPORTS 1 Turkey", country_code="tr", xmltv_id="beINSports1.tr", call_sign=""),
    DLHDChannel(number="63", name="beIN SPORTS 2 Turkey", country_code="tr", xmltv_id="beINSports2.tr", call_sign=""),
    DLHDChannel(number="64", name="beIN SPORTS 3 Turkey", country_code="tr", xmltv_id="beINSports3.tr", call_sign=""),
    DLHDChannel(
        number="65", name="Sky Sports Cricket", country_code="gb", xmltv_id="SkySportsCricket.uk", call_sign=""
    ),
    DLHDChannel(number="66", name="TUDN USA", country_code="us", xmltv_id="TUDN.us", call_sign="TUDN"),
    DLHDChannel(number="67", name="beIN SPORTS 4 Turkey", country_code="tr", xmltv_id="beINSports4.tr", call_sign=""),
    DLHDChannel(number="70", name="Sky Sports Golf UK", country_code="uk", xmltv_id="SkySportsGolf.uk", call_sign=""),
    DLHDChannel(
        number="71", name="Eleven Sports 1 Poland", country_code="pl", xmltv_id="ElevenSport1.pl", call_sign=""
    ),
    DLHDChannel(
        number="72", name="Eleven Sports 2 Poland", country_code="pl", xmltv_id="ElevenSport2.pl", call_sign=""
    ),
    DLHDChannel(
        number="73", name="Canal+ Sport 2 Poland", country_code="pl", xmltv_id="CanalPlusSport2.pl", call_sign=""
    ),
    DLHDChannel(number="74", name="Sport TV2 Portugal", country_code="pt", xmltv_id="SportTV2.pt", call_sign=""),
    DLHDChannel(number="75", name="CANAL+ SPORT 5 Poland", country_code="pl", xmltv_id="", call_sign=""),
    DLHDChannel(number="78", name="SporTV Brasil", country_code="br", xmltv_id="", call_sign=""),
    DLHDChannel(number="79", name="SporTV2 Brasil", country_code="br", xmltv_id="", call_sign=""),
    DLHDChannel(number="80", name="SporTV3 Brasil", country_code="br", xmltv_id="SporTV3.br", call_sign=""),
    DLHDChannel(number="81", name="ESPN Brasil", country_code="br", xmltv_id="ESPN.br", call_sign=""),
    DLHDChannel(number="82", name="ESPN2 Brasil", country_code="br", xmltv_id="ESPN2.br", call_sign=""),
    DLHDChannel(number="83", name="ESPN3 Brasil", country_code="br", xmltv_id="", call_sign=""),
    DLHDChannel(number="84", name="Movistar Laliga", country_code="es", xmltv_id="MLaLiga.es", call_sign=""),
    DLHDChannel(number="85", name="ESPN4 Brasil", country_code="br", xmltv_id="", call_sign=""),
    DLHDChannel(number="87", name="TNT Brasil", country_code="br", xmltv_id="TNT.br", call_sign=""),
    DLHDChannel(number="88", name="Premier Brasil", country_code="br", xmltv_id="", call_sign=""),
    DLHDChannel(number="89", name="Combate Brasil", country_code="br", xmltv_id="Combate.br", call_sign=""),
    DLHDChannel(number="90", name="beIN Sports MENA English 2", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="91", name="beIN Sports MENA 1", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="92", name="beIN Sports MENA 2", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="93", name="beIN Sports MENA 3", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="94", name="beIN Sports MENA 4", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="95", name="beIN Sports MENA 5", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="96", name="beIN Sports MENA 6", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="97", name="beIN Sports MENA 7", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="98", name="beIN Sports MENA Premium 1", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="99", name="beIN Sports MENA Premium 2", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="100", name="beIN Sports MENA Premium 3", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="101", name="Sport Klub 1 Serbia", country_code="rs", xmltv_id="SportKlub1.rs", call_sign=""),
    DLHDChannel(number="102", name="Sport Klub 2 Serbia", country_code="rs", xmltv_id="SportKlub2.rs", call_sign=""),
    DLHDChannel(number="103", name="Sport Klub 3 Serbia", country_code="rs", xmltv_id="SportKlub3.rs", call_sign=""),
    DLHDChannel(number="104", name="Sport Klub 4 Serbia", country_code="rs", xmltv_id="SportKlub4.rs", call_sign=""),
    DLHDChannel(number="111", name="TSN1", country_code="ca", xmltv_id="TSN1.ca", call_sign=""),
    DLHDChannel(number="112", name="TSN2", country_code="ca", xmltv_id="TSN2.ca", call_sign=""),
    DLHDChannel(number="113", name="TSN3", country_code="ca", xmltv_id="TSN3.ca", call_sign=""),
    DLHDChannel(number="114", name="TSN4", country_code="ca", xmltv_id="TSN4.ca", call_sign=""),
    DLHDChannel(number="115", name="TSN5", country_code="ca", xmltv_id="TSN5.ca", call_sign=""),
    DLHDChannel(number="116", name="beIN SPORTS 1 France", country_code="fr", xmltv_id="", call_sign=""),
    DLHDChannel(number="117", name="beIN SPORTS 2 France", country_code="fr", xmltv_id="", call_sign=""),
    DLHDChannel(number="118", name="beIN SPORTS 3 France", country_code="fr", xmltv_id="", call_sign=""),
    DLHDChannel(number="119", name="RMC Sport 1 France", country_code="fr", xmltv_id="RMCSport1.fr", call_sign=""),
    DLHDChannel(number="120", name="RMC Sport 2 France", country_code="fr", xmltv_id="RMCSport2.fr", call_sign=""),
    DLHDChannel(number="121", name="Canal+ France", country_code="fr", xmltv_id="CanalPlus.fr", call_sign=""),
    DLHDChannel(
        number="122", name="Canal+ Sport France", country_code="fr", xmltv_id="CanalPlusSport.fr", call_sign=""
    ),
    DLHDChannel(
        number="123", name="Astro SuperSport 1", country_code="my", xmltv_id="AstroSuperSport.my", call_sign=""
    ),
    DLHDChannel(
        number="124", name="Astro SuperSport 2", country_code="my", xmltv_id="AstroSuperSport2.my", call_sign=""
    ),
    DLHDChannel(
        number="125", name="Astro SuperSport 3", country_code="my", xmltv_id="AstroSuperSport3.my", call_sign=""
    ),
    DLHDChannel(
        number="126", name="Astro SuperSport 4", country_code="my", xmltv_id="AstroSuperSport4.my", call_sign=""
    ),
    DLHDChannel(number="127", name="Match TV Russia", country_code="ru", xmltv_id="MatchTV.ru", call_sign=""),
    DLHDChannel(number="128", name="TVP Sport Poland", country_code="pl", xmltv_id="TVPSport.pl", call_sign=""),
    DLHDChannel(
        number="129", name="Polsat Sport News Poland", country_code="pl", xmltv_id="PolsatSportNews.pl", call_sign=""
    ),
    DLHDChannel(
        number="130",
        name="Sky sports Premier League",
        country_code="uk",
        xmltv_id="SkySportsPremiereLeague.uk",
        call_sign="",
    ),
    DLHDChannel(number="131", name="Telemundo", country_code="us", xmltv_id="WKAQ.us", call_sign="WNJU"),
    DLHDChannel(number="132", name="Univision", country_code="ca", xmltv_id="UnivisionCanada.ca", call_sign=""),
    DLHDChannel(number="133", name="Unimas", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="134", name="Arena Sport 1 Premium", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="135", name="Arena Sport 2 Premium", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="136", name="Match Football 1 Russia", country_code="ru", xmltv_id="", call_sign=""),
    DLHDChannel(number="137", name="Match Football 2 Russia", country_code="ru", xmltv_id="", call_sign=""),
    DLHDChannel(number="138", name="Match Football 3 Russia", country_code="ru", xmltv_id="", call_sign=""),
    DLHDChannel(number="139", name="Arena Sport 3 Premium", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="140", name="Sport 1 Israel", country_code="il", xmltv_id="Sport1.il", call_sign=""),
    DLHDChannel(number="141", name="Sport 2 Israel", country_code="il", xmltv_id="Sport2.il", call_sign=""),
    DLHDChannel(number="142", name="Sport 3 Israel", country_code="il", xmltv_id="Sport3.il", call_sign=""),
    DLHDChannel(number="143", name="Sport 4 Israel", country_code="il", xmltv_id="Sport4.il", call_sign=""),
    DLHDChannel(number="144", name="Sport 5 Israel", country_code="il", xmltv_id="", call_sign=""),
    DLHDChannel(number="145", name="Sport 5 PLUS Israel", country_code="il", xmltv_id="", call_sign=""),
    DLHDChannel(number="146", name="Sport 5 Live Israel", country_code="il", xmltv_id="", call_sign=""),
    DLHDChannel(number="147", name="Sport 5 Star Israel", country_code="il", xmltv_id="", call_sign=""),
    DLHDChannel(number="148", name="Sport 5 Gold Israel", country_code="il", xmltv_id="", call_sign=""),
    DLHDChannel(number="149", name="ESPN SUR", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="150", name="ESPN2 SUR", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="282", name="StarzPlay CricLife 3 HD", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="283", name="StarzPlay CricLife 2 HD", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="284", name="StarzPlay CricLife 1 HD", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="288", name="ESPNews", country_code="us", xmltv_id="ESPNNews.us", call_sign="ESPNEWS"),
    DLHDChannel(number="289", name="Sport TV4 Portugal", country_code="pt", xmltv_id="SportTV4.pt", call_sign=""),
    DLHDChannel(number="290", name="Sport TV5 Portugal", country_code="pt", xmltv_id="SportTV5.pt", call_sign=""),
    DLHDChannel(number="291", name="Sport TV6 Portugal", country_code="pt", xmltv_id="SportTV6.pt", call_sign=""),
    DLHDChannel(number="292", name="NewsNation USA", country_code="us", xmltv_id="NewsNation.us", call_sign=""),
    DLHDChannel(number="293", name="Reelz Channel", country_code="us", xmltv_id="ReelzChannel.us", call_sign="REELZ"),
    DLHDChannel(number="294", name="Science Channel", country_code="us", xmltv_id="", call_sign="SCIENCE"),
    DLHDChannel(number="295", name="Adult Swim", country_code="us", xmltv_id="AdultSwim.us", call_sign="TOON"),
    DLHDChannel(
        number="296",
        name="Hallmark Movies & Mysterie",
        country_code="us",
        xmltv_id="HallmarkMoviesMysteries.us",
        call_sign="HALL",
    ),
    DLHDChannel(number="297", name="Fox Business", country_code="us", xmltv_id="FoxBusiness.us", call_sign=""),
    DLHDChannel(number="298", name="FXX USA", country_code="us", xmltv_id="FXX.us", call_sign="FXX"),
    DLHDChannel(
        number="299", name="Magnolia Network", country_code="us", xmltv_id="MagnoliaNetwork.us", call_sign="MAGN"
    ),
    DLHDChannel(number="300", name="CW USA", country_code="us", xmltv_id="", call_sign=""),
    DLHDChannel(number="301", name="Freeform", country_code="us", xmltv_id="Freeform.us", call_sign="FREEFRM"),
    DLHDChannel(number="302", name="A&E USA", country_code="us", xmltv_id="AandE.us", call_sign="AETV"),
    DLHDChannel(number="303", name="AMC USA", country_code="us", xmltv_id="AMC.us", call_sign="AMC"),
    DLHDChannel(number="304", name="Animal Planet", country_code="us", xmltv_id="AnimalPlanet.us", call_sign=""),
    DLHDChannel(number="305", name="BBC America (BBCA)", country_code="us", xmltv_id="BBCAmerica.us", call_sign="BBCA"),
    DLHDChannel(number="306", name="BET USA", country_code="us", xmltv_id="BET.us", call_sign="BET"),
    DLHDChannel(number="307", name="Bravo USA", country_code="us", xmltv_id="Bravo.us", call_sign="BRAVO"),
    DLHDChannel(
        number="308",
        name="CBS Sports Network (CBSSN)",
        country_code="us",
        xmltv_id="CBSSportsNetwork.us",
        call_sign="CBSSN",
    ),
    DLHDChannel(number="309", name="CNBC USA", country_code="us", xmltv_id="CNBC.us", call_sign="CNBC"),
    DLHDChannel(
        number="310", name="Comedy Central", country_code="us", xmltv_id="ComedyCentral.us", call_sign="COMEDYP"
    ),
    DLHDChannel(number="311", name="Discovery Life Channel", country_code="us", xmltv_id="", call_sign=""),
    DLHDChannel(number="312", name="Disney Channel", country_code="us", xmltv_id="DisneyChannel.us", call_sign="DISN"),
    DLHDChannel(
        number="313", name="Discovery Channel", country_code="us", xmltv_id="DiscoveryChannel.us", call_sign=""
    ),
    DLHDChannel(number="314", name="Disney XD", country_code="us", xmltv_id="DisneyXD.us", call_sign=""),
    DLHDChannel(
        number="315", name="E! Entertainment Television", country_code="us", xmltv_id="EEntertainment.us", call_sign="E"
    ),
    DLHDChannel(number="316", name="ESPNU USA", country_code="us", xmltv_id="ESPNU.us", call_sign="ESPNU"),
    DLHDChannel(number="317", name="FX USA", country_code="us", xmltv_id="FX.us", call_sign="FX"),
    DLHDChannel(number="318", name="GOLF Channel USA", country_code="us", xmltv_id="GolfChannel.us", call_sign="GOLF"),
    DLHDChannel(
        number="319", name="Game Show Network", country_code="us", xmltv_id="GameShowNetwork.us", call_sign="GSN"
    ),
    DLHDChannel(number="320", name="The Hallmark Channel", country_code="us", xmltv_id="", call_sign="HALL"),
    DLHDChannel(number="321", name="HBO USA", country_code="us", xmltv_id="HBO.us", call_sign="HBO"),
    DLHDChannel(number="322", name="History USA", country_code="us", xmltv_id="", call_sign="HISTORY"),
    DLHDChannel(number="323", name="Headline News", country_code="us", xmltv_id="", call_sign=""),
    DLHDChannel(
        number="324",
        name="Investigation Discovery (ID USA)",
        country_code="us",
        xmltv_id="InvestigationDiscovery.us",
        call_sign="ID",
    ),
    DLHDChannel(number="325", name="ION USA", country_code="us", xmltv_id="ION.us", call_sign="ION"),
    DLHDChannel(
        number="326", name="Lifetime Network", country_code="us", xmltv_id="LifetimeNetwork.us", call_sign="LIFE"
    ),
    DLHDChannel(number="327", name="MSNBC", country_code="us", xmltv_id="MSNBC.us", call_sign="MSNBC"),
    DLHDChannel(number="328", name="National Geographic (NGC)", country_code="us", xmltv_id="", call_sign="NGC"),
    DLHDChannel(number="329", name="NICK JR", country_code="us", xmltv_id="NickJr.us", call_sign="NICJR"),
    DLHDChannel(number="330", name="NICK", country_code="us", xmltv_id="Nickelodeon.us", call_sign="NIK"),
    DLHDChannel(
        number="331",
        name="Oprah Winfrey Network (OWN)",
        country_code="us",
        xmltv_id="OprahWinfreyNetwork.us",
        call_sign="OWN",
    ),
    DLHDChannel(number="332", name="Oxygen True Crime", country_code="us", xmltv_id="", call_sign="OXYGEN"),
    DLHDChannel(number="333", name="Showtime USA", country_code="us", xmltv_id="Showtime.us", call_sign="SHOW"),
    DLHDChannel(
        number="334", name="Paramount Network", country_code="us", xmltv_id="ParamountNetwork.us", call_sign="PAR"
    ),
    DLHDChannel(number="335", name="Starz", country_code="us", xmltv_id="Starz.us", call_sign="STARZ"),
    DLHDChannel(number="336", name="TBS USA", country_code="us", xmltv_id="TBS.us", call_sign="TBS"),
    DLHDChannel(number="337", name="TLC", country_code="us", xmltv_id="TLC.us", call_sign="TLC"),
    DLHDChannel(number="338", name="TNT USA", country_code="us", xmltv_id="TNT.us", call_sign="TNT"),
    DLHDChannel(
        number="339", name="Cartoon Network", country_code="us", xmltv_id="CartoonNetwork.us", call_sign="TOON"
    ),
    DLHDChannel(number="340", name="Travel Channel", country_code="us", xmltv_id="TravelChannel.us", call_sign="TRAV"),
    DLHDChannel(number="341", name="TruTV USA", country_code="us", xmltv_id="truTV.us", call_sign="TRUTV"),
    DLHDChannel(number="342", name="TVLAND", country_code="us", xmltv_id="", call_sign="TVLAND"),
    DLHDChannel(number="343", name="USA Network", country_code="us", xmltv_id="USANetwork.us", call_sign="USA"),
    DLHDChannel(number="344", name="VH1 USA", country_code="us", xmltv_id="VH1.us", call_sign="VH1"),
    DLHDChannel(number="345", name="CNN USA", country_code="us", xmltv_id="CNN.us", call_sign="CNN"),
    DLHDChannel(number="346", name="Willow Cricket", country_code="", xmltv_id="WillowCricket.us", call_sign=""),
    DLHDChannel(number="347", name="Fox News", country_code="us", xmltv_id="FoxNews.us", call_sign=""),
    DLHDChannel(number="348", name="Dave", country_code="uk", xmltv_id="Dave.uk", call_sign=""),
    DLHDChannel(number="349", name="BBC News Channel HD", country_code="uk", xmltv_id="", call_sign=""),
    DLHDChannel(number="350", name="ITV 1 UK", country_code="uk", xmltv_id="ITV1.uk", call_sign=""),
    DLHDChannel(number="351", name="ITV 2 UK", country_code="uk", xmltv_id="ITV2.uk", call_sign=""),
    DLHDChannel(number="352", name="ITV 3 UK", country_code="uk", xmltv_id="ITV3.uk", call_sign=""),
    DLHDChannel(number="353", name="ITV 4 UK", country_code="uk", xmltv_id="ITV4.uk", call_sign=""),
    DLHDChannel(number="354", name="Channel 4 UK", country_code="uk", xmltv_id="Channel4.uk", call_sign=""),
    DLHDChannel(number="355", name="Channel 5 UK", country_code="uk", xmltv_id="Channel5.uk", call_sign=""),
    DLHDChannel(number="356", name="BBC One UK", country_code="uk", xmltv_id="BBC1.uk", call_sign=""),
    DLHDChannel(number="357", name="BBC Two UK", country_code="uk", xmltv_id="BBC2.uk", call_sign=""),
    DLHDChannel(number="358", name="BBC Three UK", country_code="uk", xmltv_id="BBC3.uk", call_sign=""),
    DLHDChannel(number="359", name="BBC Four UK", country_code="uk", xmltv_id="BBC4.uk", call_sign=""),
    DLHDChannel(number="360", name="5 USA", country_code="us", xmltv_id="", call_sign=""),
    DLHDChannel(number="361", name="Sky Witness HD", country_code="gb", xmltv_id="SkyWitness.uk", call_sign=""),
    DLHDChannel(number="362", name="Sky Atlantic", country_code="gb", xmltv_id="SkyAtlantic.uk", call_sign=""),
    DLHDChannel(number="363", name="E4 Channel", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="364", name="RTE 1", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="365", name="RTE 2", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="366", name="Sky Sports News UK", country_code="uk", xmltv_id="SkySportsNews.uk", call_sign=""),
    DLHDChannel(number="367", name="MTV UK", country_code="uk", xmltv_id="MTV.uk", call_sign=""),
    DLHDChannel(
        number="368", name="SuperSport Cricket", country_code="za", xmltv_id="SuperSportCricket.za", call_sign=""
    ),
    DLHDChannel(number="369", name="Fox Cricket", country_code="au", xmltv_id="FoxSports1.au", call_sign=""),
    DLHDChannel(number="370", name="Astro Cricket", country_code="my", xmltv_id="AstroCricket.my", call_sign=""),
    DLHDChannel(number="371", name="MTV USA", country_code="us", xmltv_id="MTV.us", call_sign="MTV"),
    DLHDChannel(number="372", name="beIN SPORTS en Español", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="373", name="SYFY USA", country_code="us", xmltv_id="Syfy.us", call_sign="SYFY"),
    DLHDChannel(number="374", name="Cinemax USA", country_code="us", xmltv_id="Cinemax.us", call_sign=""),
    DLHDChannel(number="375", name="ESPN Deportes", country_code="", xmltv_id="ESPNDeportes.us", call_sign=""),
    DLHDChannel(number="376", name="WWE Network", country_code="us", xmltv_id="WWE.us", call_sign=""),
    DLHDChannel(number="377", name="MUTV UK", country_code="uk", xmltv_id="MUTV.uk", call_sign=""),
    DLHDChannel(number="378", name="Veronica NL Netherland", country_code="nl", xmltv_id="", call_sign=""),
    DLHDChannel(number="379", name="ESPN 1 NL", country_code="nl", xmltv_id="ESPN1.nl", call_sign=""),
    DLHDChannel(number="380", name="Benfica TV PT", country_code="pt", xmltv_id="BenficaTV1.pt", call_sign=""),
    DLHDChannel(
        number="381", name="FX Movie Channel", country_code="us", xmltv_id="FXMovieChannel.us", call_sign="FXM"
    ),
    DLHDChannel(number="382", name="HGTV", country_code="us", xmltv_id="HGTV.us", call_sign="HGTV"),
    DLHDChannel(
        number="383", name="Ziggo Sport Docu NL", country_code="nl", xmltv_id="ZiggoSportDocu.nl", call_sign=""
    ),
    DLHDChannel(number="384", name="The Food Network", country_code="us", xmltv_id="FoodNetwork.us", call_sign="FOOD"),
    DLHDChannel(number="385", name="SEC Network USA", country_code="us", xmltv_id="SECNetwork.us", call_sign="SEC"),
    DLHDChannel(number="386", name="ESPN 2 NL", country_code="nl", xmltv_id="ESPN2.nl", call_sign=""),
    DLHDChannel(number="387", name="ESPN Premium Argentina", country_code="ar", xmltv_id="", call_sign=""),
    DLHDChannel(number="388", name="TNT Sports Argentina", country_code="ar", xmltv_id="TNTSports.ar", call_sign=""),
    DLHDChannel(
        number="389",
        name="Lifetime Movies Network",
        country_code="us",
        xmltv_id="LifetimeMovieNetwork.us",
        call_sign="LIFE",
    ),
    DLHDChannel(number="390", name="RTL7 Netherland", country_code="nl", xmltv_id="RTL7.nl", call_sign=""),
    DLHDChannel(number="391", name="VTV+ Uruguay", country_code="uy", xmltv_id="", call_sign=""),
    DLHDChannel(
        number="392", name="Win Sports+ Columbia", country_code="co", xmltv_id="WinSportsPlus.co", call_sign=""
    ),
    DLHDChannel(
        number="393", name="Ziggo Sport Select NL", country_code="nl", xmltv_id="ZiggoSportSelect.nl", call_sign=""
    ),
    DLHDChannel(
        number="394", name="The Weather Channel", country_code="us", xmltv_id="WeatherChannel.us", call_sign="WEATH"
    ),
    DLHDChannel(number="395", name="МАТЧ! БОЕЦ Russia", country_code="ru", xmltv_id="", call_sign=""),
    DLHDChannel(
        number="396", name="Ziggo Sport Racing NL", country_code="nl", xmltv_id="ZiggoSportRacing.nl", call_sign=""
    ),
    DLHDChannel(
        number="397", name="BIG TEN Network (BTN USA)", country_code="us", xmltv_id="BigTenNetwork.us", call_sign=""
    ),
    DLHDChannel(
        number="398", name="Ziggo Sport Voetbal NL", country_code="n;", xmltv_id="ZiggoSportVoetbal.nl", call_sign=""
    ),
    DLHDChannel(number="399", name="MLB Network USA", country_code="us", xmltv_id="MLBNetwork.us", call_sign="MLBN"),
    DLHDChannel(number="400", name="Digi Sport 1 Romania", country_code="ro", xmltv_id="DigiSport1.ro", call_sign=""),
    DLHDChannel(number="401", name="Digi Sport 2 Romania", country_code="ro", xmltv_id="DigiSport2.ro", call_sign=""),
    DLHDChannel(number="402", name="Digi Sport 3 Romania", country_code="ro", xmltv_id="DigiSport3.ro", call_sign=""),
    DLHDChannel(number="403", name="Digi Sport 4 Romania", country_code="ro", xmltv_id="DigiSport4.ro", call_sign=""),
    DLHDChannel(number="404", name="NBA TV USA", country_code="us", xmltv_id="NBATV.us", call_sign="NBATV"),
    DLHDChannel(number="405", name="NFL Network", country_code="us", xmltv_id="NFLNetwork.us", call_sign="NFLNET"),
    DLHDChannel(
        number="406", name="Sportsnet Ontario", country_code="ca", xmltv_id="SportsnetOntario.ca", call_sign=""
    ),
    DLHDChannel(number="407", name="Sportsnet West", country_code="ca", xmltv_id="SportsnetWest.ca", call_sign=""),
    DLHDChannel(number="408", name="Sportsnet East", country_code="ca", xmltv_id="SportsnetEast.ca", call_sign=""),
    DLHDChannel(number="409", name="Sportsnet 360", country_code="ca", xmltv_id="Sportsnet360.ca", call_sign=""),
    DLHDChannel(number="410", name="Sportsnet World", country_code="ca", xmltv_id="SportsnetWorld.ca", call_sign=""),
    DLHDChannel(number="411", name="Sportsnet One", country_code="ca", xmltv_id="SportsnetOne.ca", call_sign=""),
    DLHDChannel(
        number="412", name="SuperSport Grandstand", country_code="za", xmltv_id="SuperSportGrandstand.za", call_sign=""
    ),
    DLHDChannel(number="413", name="SuperSport PSL", country_code="za", xmltv_id="SuperSportPSL.za", call_sign=""),
    DLHDChannel(
        number="414",
        name="SuperSport Premier league",
        country_code="ng",
        xmltv_id="SupersportPremierLeague.ng",
        call_sign="",
    ),
    DLHDChannel(
        number="415", name="SuperSport LaLiga", country_code="za", xmltv_id="SuperSportLaLiga.za", call_sign=""
    ),
    DLHDChannel(
        number="416", name="SuperSport Variety 1", country_code="za", xmltv_id="SuperSportVariety1.za", call_sign=""
    ),
    DLHDChannel(
        number="417", name="SuperSport Variety 2", country_code="za", xmltv_id="SuperSportVariety2.za", call_sign=""
    ),
    DLHDChannel(
        number="418", name="SuperSport Variety 3", country_code="za", xmltv_id="SuperSportVariety3", call_sign=""
    ),
    DLHDChannel(
        number="419", name="SuperSport Variety 4", country_code="za", xmltv_id="SuperSportVariety4.za", call_sign=""
    ),
    DLHDChannel(
        number="420", name="SuperSport Action", country_code="za", xmltv_id="SuperSportAction.za", call_sign=""
    ),
    DLHDChannel(number="421", name="SuperSport Rugby", country_code="za", xmltv_id="SuperSportRugby.za", call_sign=""),
    DLHDChannel(number="422", name="SuperSport Golf", country_code="za", xmltv_id="SuperSportGolf.za", call_sign=""),
    DLHDChannel(
        number="423", name="SuperSport Tennis", country_code="za", xmltv_id="SuperSportTennis.za", call_sign=""
    ),
    DLHDChannel(
        number="424", name="SuperSport Motorsport", country_code="za", xmltv_id="SuperSportMotorsport.za", call_sign=""
    ),
    DLHDChannel(number="425", name="BeIN SPORTS USA", country_code="us", xmltv_id="", call_sign="BEINS1"),
    DLHDChannel(number="426", name="DAZN 1 Bar DE", country_code="de", xmltv_id="DAZN1.de", call_sign=""),
    DLHDChannel(number="427", name="DAZN 2 Bar DE", country_code="de", xmltv_id="DAZN2.de", call_sign=""),
    DLHDChannel(
        number="428", name="Eleven Sports 3 Poland", country_code="pl", xmltv_id="ElevenSport3.pl", call_sign=""
    ),
    DLHDChannel(number="429", name="Arena Sport 1 Serbia", country_code="rs", xmltv_id="Arenasport1.rs", call_sign=""),
    DLHDChannel(number="430", name="Arena Sport 2 Serbia", country_code="rs", xmltv_id="Arenasport2.rs", call_sign=""),
    DLHDChannel(number="431", name="Arena Sport 3 Serbia", country_code="rs", xmltv_id="Arenasport3.rs", call_sign=""),
    DLHDChannel(number="432", name="Arena Sport 1 Croatia", country_code="hr", xmltv_id="ArenaSport1.hr", call_sign=""),
    DLHDChannel(number="433", name="Arena Sport 2 Croatia", country_code="hr", xmltv_id="ArenaSport2.hr", call_sign=""),
    DLHDChannel(number="434", name="Arena Sport 3 Croatia", country_code="hr", xmltv_id="ArenaSport3.hr", call_sign=""),
    DLHDChannel(
        number="435", name="Movistar Liga de Campeones", country_code="es", xmltv_id="LigadeCampeones1.es", call_sign=""
    ),
    DLHDChannel(
        number="436", name="Movistar Deportes Spain", country_code="es", xmltv_id="MovistarDeportes1.es", call_sign=""
    ),
    DLHDChannel(number="437", name="#0 Spain", country_code="rs", xmltv_id="", call_sign=""),
    DLHDChannel(
        number="438", name="Movistar Deportes 2 Spain", country_code="rs", xmltv_id="MovistarDeportes2.es", call_sign=""
    ),
    DLHDChannel(
        number="439", name="Orange Sport 1 Romania", country_code="ro", xmltv_id="OrangeSport1.ro", call_sign=""
    ),
    DLHDChannel(
        number="440", name="Orange Sport 2 Romania", country_code="ro", xmltv_id="OrangeSport2.ro", call_sign=""
    ),
    DLHDChannel(
        number="441", name="Orange Sport 3 Romania", country_code="ro", xmltv_id="OrangeSport3.ro", call_sign=""
    ),
    DLHDChannel(
        number="442", name="Orange Sport 4 Romania", country_code="ro", xmltv_id="OrangeSport4.ro", call_sign=""
    ),
    DLHDChannel(number="443", name="Polsat News Poland", country_code="pl", xmltv_id="PolsatNews.pl", call_sign=""),
    DLHDChannel(number="444", name="TVN24 Poland", country_code="pl", xmltv_id="TVN24.pl", call_sign=""),
    DLHDChannel(number="445", name="DAZN 1 Spain", country_code="es", xmltv_id="DAZN1.es", call_sign=""),
    DLHDChannel(number="446", name="DAZN 2 Spain", country_code="es", xmltv_id="DAZN2.es", call_sign=""),
    DLHDChannel(number="447", name="DAZN 3 Spain", country_code="es", xmltv_id="DAZN3.es", call_sign=""),
    DLHDChannel(number="448", name="DAZN 4 Spain", country_code="es", xmltv_id="DAZN4.es", call_sign=""),
    DLHDChannel(number="449", name="Sky Sports MIX UK", country_code="gb", xmltv_id="SkySportsMix.uk", call_sign=""),
    DLHDChannel(number="450", name="PTV Sports", country_code="pk", xmltv_id="PTVSport.pk", call_sign=""),
    DLHDChannel(
        number="451", name="Viaplay Sports 1 UK", country_code="uk", xmltv_id="ViaplaySports1.uk", call_sign=""
    ),
    DLHDChannel(number="452", name="TVP INFO", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="453", name="Sport Klub HD Serbia", country_code="rs", xmltv_id="", call_sign=""),
    DLHDChannel(number="454", name="Sport TV3 Portugal", country_code="pt", xmltv_id="SportTV3.pt", call_sign=""),
    DLHDChannel(
        number="455", name="Eleven Sports 1 Portugal", country_code="pt", xmltv_id="ElevenSports1.pt", call_sign=""
    ),
    DLHDChannel(
        number="456", name="Eleven Sports 2 Portugal", country_code="pt", xmltv_id="ElevenSports2.pt", call_sign=""
    ),
    DLHDChannel(
        number="457", name="Eleven Sports 3 Portugal", country_code="pt", xmltv_id="ElevenSports3.pt", call_sign=""
    ),
    DLHDChannel(
        number="458", name="Eleven Sports 4 Portugal", country_code="pt", xmltv_id="ElevenSports4.pt", call_sign=""
    ),
    DLHDChannel(
        number="459", name="Eleven Sports 5 Portugal", country_code="pt", xmltv_id="ElevenSports5.pt", call_sign=""
    ),
    DLHDChannel(
        number="460", name="Sky Sport Football Italy", country_code="it", xmltv_id="SkySportFootball.it", call_sign=""
    ),
    DLHDChannel(number="461", name="Sky Sport UNO Italy", country_code="it", xmltv_id="SkySportUno.it", call_sign=""),
    DLHDChannel(
        number="462", name="Sky Sport Arena Italy", country_code="it", xmltv_id="SkySportArena.it", call_sign=""
    ),
    DLHDChannel(number="463", name="Canal+ Foot France", country_code="fr", xmltv_id="CanalPlusFoot.fr", call_sign=""),
    DLHDChannel(number="464", name="Canal+ Sport360", country_code="fr", xmltv_id="CanalPlusSport360.fr", call_sign=""),
    DLHDChannel(number="465", name="Diema Sport Bulgaria", country_code="bg", xmltv_id="DiemaSport.bg", call_sign=""),
    DLHDChannel(
        number="466", name="Diema Sport 2 Bulgaria", country_code="bg", xmltv_id="DiemaSport2.bg", call_sign=""
    ),
    DLHDChannel(
        number="467", name="Diema Sport 3 Bulgaria", country_code="bg", xmltv_id="DiemaSport3.bg", call_sign=""
    ),
    DLHDChannel(number="468", name="Nova Sport Bulgaria", country_code="bg", xmltv_id="NovaSport.bg", call_sign=""),
    DLHDChannel(number="469", name="Eurosport 1 Bulgaria", country_code="bg", xmltv_id="Eurosport1.bg", call_sign=""),
    DLHDChannel(number="470", name="Eurosport 2 Bulgaria", country_code="bg", xmltv_id="Eurosport2.bg", call_sign=""),
    DLHDChannel(number="471", name="Ring Bulgaria", country_code="bg", xmltv_id="", call_sign=""),
    DLHDChannel(number="472", name="Max Sport 1 Bulgaria", country_code="bg", xmltv_id="MAXSport1.bg", call_sign=""),
    DLHDChannel(number="473", name="Max Sport 2 Bulgaria", country_code="bg", xmltv_id="MAXSport2.bg", call_sign=""),
    DLHDChannel(number="474", name="Max Sport 3 Bulgaria", country_code="bg", xmltv_id="MAXSport3.bg", call_sign=""),
    DLHDChannel(number="475", name="Max Sport 4 Bulgaria", country_code="bg", xmltv_id="MAXSport4.bg", call_sign=""),
    DLHDChannel(number="476", name="BNT 1 Bulgaria", country_code="bg", xmltv_id="BNT1.bg", call_sign=""),
    DLHDChannel(number="477", name="BNT 2 Bulgaria", country_code="bg", xmltv_id="BNT2.bg", call_sign=""),
    DLHDChannel(number="478", name="BNT 3 Bulgaria", country_code="bg", xmltv_id="", call_sign=""),
    DLHDChannel(number="478", name="BNT 3 Bulgaria", country_code="bg", xmltv_id="", call_sign=""),
    DLHDChannel(number="479", name="bTV Bulgaria", country_code="bg", xmltv_id="bTV.bg", call_sign=""),
    DLHDChannel(number="480", name="Nova TV Bulgaria", country_code="bg", xmltv_id="", call_sign=""),
    DLHDChannel(number="481", name="bTV Action Bulgaria", country_code="bg", xmltv_id="bTVAction.bg", call_sign=""),
    DLHDChannel(number="482", name="Diema Bulgaria", country_code="bg", xmltv_id="Diema.bg", call_sign=""),
    DLHDChannel(number="483", name="FOX HD Bulgaria", country_code="bg", xmltv_id="", call_sign=""),
    DLHDChannel(number="484", name="bTV Lady Bulgaria", country_code="bg", xmltv_id="bTVLady.bg", call_sign=""),
    DLHDChannel(number="485", name="Diema Family Bulgaria", country_code="bg", xmltv_id="DiemaFamily.bg", call_sign=""),
    DLHDChannel(
        number="486", name="Canal+ Sport 1 Afrique", country_code="ke", xmltv_id="CanalPlusSport1.ke", call_sign=""
    ),
    DLHDChannel(
        number="487", name="Canal+ Sport 2 Afrique", country_code="ke", xmltv_id="CanalPlusSport2.ke", call_sign=""
    ),
    DLHDChannel(
        number="488", name="Canal+ Sport 3 Afrique", country_code="ke", xmltv_id="CanalPlusSport3.ke", call_sign=""
    ),
    DLHDChannel(
        number="489", name="Canal+ Sport 4 Afrique", country_code="ke", xmltv_id="CanalPlusSport4.ke", call_sign=""
    ),
    DLHDChannel(
        number="490", name="Canal+ Sport 5 Afrique", country_code="ke", xmltv_id="CanalPlusSport5.ke", call_sign=""
    ),
    DLHDChannel(number="491", name="beIN SPORTS Australia 1", country_code="au", xmltv_id="", call_sign=""),
    DLHDChannel(number="492", name="beIN SPORTS Australia 2", country_code="au", xmltv_id="", call_sign=""),
    DLHDChannel(number="493", name="beIN SPORTS Australia 3", country_code="au", xmltv_id="", call_sign=""),
    DLHDChannel(number="494", name="beIN Sports MAX 4 France", country_code="fr", xmltv_id="", call_sign=""),
    DLHDChannel(number="495", name="beIN Sports MAX 5 France", country_code="fr", xmltv_id="", call_sign=""),
    DLHDChannel(number="496", name="beIN Sports MAX 6 France", country_code="fr", xmltv_id="", call_sign=""),
    DLHDChannel(number="497", name="beIN Sports MAX 7 France", country_code="fr", xmltv_id="", call_sign=""),
    DLHDChannel(number="498", name="beIN Sports MAX 8 France", country_code="fr", xmltv_id="", call_sign=""),
    DLHDChannel(number="499", name="beIN Sports MAX 9 France", country_code="fr", xmltv_id="", call_sign=""),
    DLHDChannel(number="500", name="beIN Sports MAX 10 France", country_code="fr", xmltv_id="", call_sign=""),
    DLHDChannel(number="501", name="18+ (Player-01)", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="502", name="18+ (Player-02)", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="503", name="18+ (Player-03)", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="504", name="18+ (Player-04)", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="505", name="18+ (Player-05)", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="506", name="18+ (Player-06)", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="507", name="18+ (Player-07)", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="508", name="18+ (Player-08)", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="509", name="18+ (Player-09)", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="510", name="18+ (Player-10)", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="511", name="18+ (Player-11)", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="512", name="18+ (Player-12)", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="513", name="18+ (Player-13)", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="514", name="18+ (Player-14)", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="515", name="18+ (Player-15)", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="516", name="18+ (Player-16)", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="517", name="18+ (Player-17)", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="518", name="18+ (Player-18)", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="519", name="18+ (Player-19)", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="520", name="18+ (Player-20)", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="521", name="#Vamos Spain", country_code="es", xmltv_id="Vamos.es", call_sign=""),
    DLHDChannel(number="522", name="Barca TV Spain", country_code="es", xmltv_id="", call_sign=""),
    DLHDChannel(number="523", name="Real Madrid TV Spain", country_code="es", xmltv_id="RealMadridTV.es", call_sign=""),
    DLHDChannel(number="524", name="EuroSport 1 Spain", country_code="es", xmltv_id="Eurosport1.es", call_sign=""),
    DLHDChannel(number="525", name="EuroSport 2 Spain", country_code="es", xmltv_id="Eurosport2.es", call_sign=""),
    DLHDChannel(
        number="526", name="Movistar Deportes 3 Spain", country_code="es", xmltv_id="MovistarDeportes3.es", call_sign=""
    ),
    DLHDChannel(number="527", name="Movistar Deportes 4 Spain", country_code="es", xmltv_id="", call_sign=""),
    DLHDChannel(number="527", name="Movistar Deportes 4 Spain", country_code="es", xmltv_id="", call_sign=""),
    DLHDChannel(number="528", name="Movistar Golf Spain", country_code="es", xmltv_id="MovistarGolf.es", call_sign=""),
    DLHDChannel(
        number="529", name="Teledeporte Spain (TDP)", country_code="es", xmltv_id="Teledeporte.es", call_sign=""
    ),
    DLHDChannel(number="530", name="GOL PLAY Spain", country_code="es", xmltv_id="", call_sign=""),
    DLHDChannel(number="531", name="Antena 3 Spain", country_code="es", xmltv_id="Antena3.es", call_sign=""),
    DLHDChannel(number="532", name="Telecinco Spain", country_code="es", xmltv_id="Telecinco.es", call_sign=""),
    DLHDChannel(number="533", name="TVE La 1 Spain", country_code="es", xmltv_id="", call_sign=""),
    DLHDChannel(number="534", name="La Sexta Spain", country_code="es", xmltv_id="LaSexta.es", call_sign=""),
    DLHDChannel(number="535", name="Cuatro Spain", country_code="es", xmltv_id="Cuatro.es", call_sign=""),
    DLHDChannel(number="536", name="TVE La 2 Spain", country_code="es", xmltv_id="", call_sign=""),
    DLHDChannel(number="537", name="DAZN F1 ES", country_code="es", xmltv_id="DAZNF1.es", call_sign=""),
    DLHDChannel(number="538", name="DAZN LaLiga", country_code="es", xmltv_id="DaznLaLiga.es", call_sign=""),
    DLHDChannel(
        number="539", name="LaLiga SmartBank TV", country_code="es", xmltv_id="LaLigaSmartBank1.es", call_sign=""
    ),
    DLHDChannel(number="540", name="Canal 11 Portugal", country_code="pt", xmltv_id="Canal11.pt", call_sign=""),
    DLHDChannel(number="541", name="ONE 1 HD Israel", country_code="il", xmltv_id="", call_sign=""),
    DLHDChannel(number="542", name="ONE 2 HD Israel", country_code="il", xmltv_id="", call_sign=""),
    DLHDChannel(
        number="543", name="Yes Movies Action Israel", country_code="il", xmltv_id="YesMoviesAction.il", call_sign=""
    ),
    DLHDChannel(
        number="544", name="Yes Movies Kids Israel", country_code="il", xmltv_id="YesMoviesKids.il", call_sign=""
    ),
    DLHDChannel(
        number="545", name="Yes Movies Comedy Israel", country_code="il", xmltv_id="YesMoviesComedy.il", call_sign=""
    ),
    DLHDChannel(number="546", name="Channel 9 Israel", country_code="il", xmltv_id="Channel9.il", call_sign=""),
    DLHDChannel(number="547", name="Channel 10 Israe", country_code="il", xmltv_id="", call_sign=""),
    DLHDChannel(number="548", name="Channel 11 Israel", country_code="il", xmltv_id="", call_sign=""),
    DLHDChannel(number="549", name="Channel 12 Israel", country_code="il", xmltv_id="", call_sign=""),
    DLHDChannel(
        number="550", name="Viaplay Sports 2 UK", country_code="uk", xmltv_id="ViaplaySports2.uk", call_sign=""
    ),
    DLHDChannel(number="551", name="Channel 13 Israel", country_code="il", xmltv_id="", call_sign=""),
    DLHDChannel(number="552", name="Channel 14 Israel", country_code="il", xmltv_id="", call_sign=""),
    DLHDChannel(number="553", name="HOT3 Israel", country_code="il", xmltv_id="HOT3.il", call_sign=""),
    DLHDChannel(
        number="554", name="Sky Sports Racing UK", country_code="uk", xmltv_id="SkySportsRacing.uk", call_sign=""
    ),
    DLHDChannel(number="555", name="Racing Tv UK", country_code="gb", xmltv_id="RacingUK.uk", call_sign=""),
    DLHDChannel(
        number="556", name="Sky Sport Top Event DE", country_code="de", xmltv_id="SkySportTopEvent.de", call_sign=""
    ),
    DLHDChannel(number="557", name="Sky Sport Mix DE", country_code="de", xmltv_id="SkySportMix.de", call_sign=""),
    DLHDChannel(
        number="558", name="Sky Sport Bundesliga 1 HD", country_code="de", xmltv_id="SkyBundesliga1.de", call_sign=""
    ),
    DLHDChannel(
        number="559", name="Sky Sport Austria 1 HD", country_code="at", xmltv_id="SkySportAustria1.at", call_sign=""
    ),
    DLHDChannel(number="560", name="TVP1 Poland", country_code="pl", xmltv_id="TVP1.pl", call_sign=""),
    DLHDChannel(number="561", name="TVP2 Poland", country_code="pl", xmltv_id="TVP2.pl", call_sign=""),
    DLHDChannel(number="562", name="Polsat Poland", country_code="pl", xmltv_id="Polsat.pl", call_sign=""),
    DLHDChannel(number="563", name="Motowizja Poland", country_code="pl", xmltv_id="MotowizjaTV.pl", call_sign=""),
    DLHDChannel(number="564", name="Polsat Film Poland", country_code="pl", xmltv_id="PolsatFilm.pl", call_sign=""),
    DLHDChannel(number="565", name="TVN HD Poland", country_code="pl", xmltv_id="TVN.pl", call_sign=""),
    DLHDChannel(
        number="566", name="Canal+ Premium Poland", country_code="pl", xmltv_id="CanalPlusPremium.pl", call_sign=""
    ),
    DLHDChannel(
        number="567", name="Canal+ Family Poland", country_code="pl", xmltv_id="CanalPlusFamily.pl", call_sign=""
    ),
    DLHDChannel(
        number="568", name="FilmBox Premium Poland", country_code="pl", xmltv_id="FilmboxPremium.pl", call_sign=""
    ),
    DLHDChannel(number="569", name="HBO Poland", country_code="pl", xmltv_id="HBO.pl", call_sign=""),
    DLHDChannel(
        number="570", name="Canal+ Seriale Poland", country_code="pl", xmltv_id="CanalPlusSeriale.pl", call_sign=""
    ),
    DLHDChannel(
        number="571", name="SportDigital Fussball", country_code="de", xmltv_id="sportdigital.de", call_sign=""
    ),
    DLHDChannel(
        number="572", name="SuperSport MaXimo 1", country_code="za", xmltv_id="SuperSportMaximo1.za", call_sign=""
    ),
    DLHDChannel(number="573", name="Match Premier Russia", country_code="ru", xmltv_id="MatchPremier.ru", call_sign=""),
    DLHDChannel(
        number="574", name="Sky Sports Golf Italy", country_code="it", xmltv_id="SkySportGolf.it", call_sign=""
    ),
    DLHDChannel(
        number="575", name="Sky Sport MotoGP Italy", country_code="it", xmltv_id="SkySportMotoGP.it", call_sign=""
    ),
    DLHDChannel(
        number="576", name="Sky Sport Tennis Italy", country_code="it", xmltv_id="SkySportTennis.it", call_sign=""
    ),
    DLHDChannel(number="577", name="Sky Sport F1 Italy", country_code="it", xmltv_id="SkySportF1.it", call_sign=""),
    DLHDChannel(number="578", name="BeIN Sports HD Qatar", country_code="qa", xmltv_id="", call_sign=""),
    DLHDChannel(number="579", name="Arena Sport 1 BiH", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="580", name="Arena Sport 4 Croatia", country_code="hr", xmltv_id="ArenaSport4.hr", call_sign=""),
    DLHDChannel(number="581", name="Arena Sport 4 Serbia", country_code="rs", xmltv_id="Arenasport4.rs", call_sign=""),
    DLHDChannel(number="582", name="Nova Sport Serbia", country_code="rs", xmltv_id="NovaSport.rs", call_sign=""),
    DLHDChannel(number="583", name="Prima Sport 1", country_code="ro", xmltv_id="PrimaSport1.ro", call_sign=""),
    DLHDChannel(number="584", name="Prima Sport 2", country_code="ro", xmltv_id="PrimaSport2.ro", call_sign=""),
    DLHDChannel(number="585", name="Prima Sport 3", country_code="ro", xmltv_id="PrimaSport3.ro", call_sign=""),
    DLHDChannel(number="586", name="Prima Sport 4", country_code="ro", xmltv_id="PrimaSport4.ro", call_sign=""),
    DLHDChannel(
        number="587", name="Sky Sport Select NZ", country_code="nz", xmltv_id="SkySportSelect.nz", call_sign=""
    ),
    DLHDChannel(number="588", name="Sky Sport 1 NZ", country_code="nz", xmltv_id="SkySport1.nz", call_sign=""),
    DLHDChannel(number="589", name="Sky Sport 2 NZ", country_code="nz", xmltv_id="SkySport2.nz", call_sign=""),
    DLHDChannel(number="590", name="Sky Sport 3 NZ", country_code="nz", xmltv_id="SkySport3.nz", call_sign=""),
    DLHDChannel(number="591", name="Sky Sport 4 NZ", country_code="nz", xmltv_id="SkySport4.nz", call_sign=""),
    DLHDChannel(number="592", name="Sky Sport 5 NZ", country_code="nz", xmltv_id="SkySport5.nz", call_sign=""),
    DLHDChannel(number="593", name="Sky Sport 6 NZ", country_code="nz", xmltv_id="SkySport6.nz", call_sign=""),
    DLHDChannel(number="594", name="Sky Sport 7 NZ", country_code="nz", xmltv_id="SkySport7.nz", call_sign=""),
    DLHDChannel(number="595", name="Sky Sport 8 NZ", country_code="nz", xmltv_id="SkySport8.nz", call_sign=""),
    DLHDChannel(number="596", name="Sky Sport 9 NZ", country_code="nz", xmltv_id="SkySport9.nz", call_sign=""),
    DLHDChannel(number="597", name="Viaplay Xtra UK", country_code="uk", xmltv_id="ViaplayXtra.uk", call_sign=""),
    DLHDChannel(number="598", name="Willow XTRA", country_code="us", xmltv_id="WILLX.us", call_sign="WILLOW"),
    DLHDChannel(number="599", name="Nova Sports Premier League Greece", country_code="gr", xmltv_id="", call_sign=""),
    DLHDChannel(
        number="600", name="Abu Dhabi Sports 1 UAE", country_code="ae", xmltv_id="AbuDhabiSports1.ae", call_sign=""
    ),
    DLHDChannel(
        number="601", name="Smithsonian Channel", country_code="us", xmltv_id="SmithsonianChannel.us", call_sign=""
    ),
    DLHDChannel(number="602", name="CTV Canada", country_code="ca", xmltv_id="", call_sign=""),
    DLHDChannel(number="604", name="Dubai Sports 1 UAE", country_code="ae", xmltv_id="DubaiSports1En.ae", call_sign=""),
    DLHDChannel(number="605", name="Dubai Sports 2 UAE", country_code="ae", xmltv_id="DubaiSports2En.ae", call_sign=""),
    DLHDChannel(number="606", name="Dubai Sports 3 UAE", country_code="ae", xmltv_id="", call_sign=""),
    DLHDChannel(number="607", name="Dubai Racing 1 UAE", country_code="ae", xmltv_id="DubaiRacingEn.ae", call_sign=""),
    DLHDChannel(number="608", name="Dubai Racing 2 UAE", country_code="ae", xmltv_id="", call_sign=""),
    DLHDChannel(number="609", name="Yas TV UAE", country_code="ae", xmltv_id="", call_sign=""),
    DLHDChannel(
        number="610",
        name="Abu Dhabi Sports 2 Premium",
        country_code="ae",
        xmltv_id="AbuDhabiSports2PremiumEn.ae",
        call_sign="",
    ),
    DLHDChannel(number="611", name="OnTime Sports", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="612", name="OnTime Sports 2", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="613", name="Newsmax USA", country_code="us", xmltv_id="Newsmax.us", call_sign="NEWSMX"),
    DLHDChannel(number="614", name="SSC Sport 1", country_code="sa", xmltv_id="", call_sign=""),
    DLHDChannel(number="615", name="SSC Sport 2", country_code="sa", xmltv_id="", call_sign=""),
    DLHDChannel(number="616", name="SSC Sport 3", country_code="sa", xmltv_id="", call_sign=""),
    DLHDChannel(number="617", name="SSC Sport 4", country_code="sa", xmltv_id="", call_sign=""),
    DLHDChannel(number="618", name="SSC Sport 5", country_code="sa", xmltv_id="", call_sign=""),
    DLHDChannel(number="619", name="SSC Sport Extra 1", country_code="sa", xmltv_id="", call_sign=""),
    DLHDChannel(number="620", name="SSC Sport Extra 2", country_code="sa", xmltv_id="", call_sign=""),
    DLHDChannel(number="621", name="SSC Sport Extra 3", country_code="sa", xmltv_id="", call_sign=""),
    DLHDChannel(number="622", name="Cosmote Sport 1 HD", country_code="gr", xmltv_id="CosmoteSport1.gr", call_sign=""),
    DLHDChannel(number="623", name="Cosmote Sport 2 HD", country_code="gr", xmltv_id="CosmoteSport2.gr", call_sign=""),
    DLHDChannel(number="624", name="Cosmote Sport 3 HD", country_code="gr", xmltv_id="CosmoteSport3.gr", call_sign=""),
    DLHDChannel(number="625", name="Cosmote Sport 4 HD", country_code="gr", xmltv_id="CosmoteSport4.gr", call_sign=""),
    DLHDChannel(number="626", name="Cosmote Sport 5 HD", country_code="gr", xmltv_id="CosmoteSport5.gr", call_sign=""),
    DLHDChannel(number="627", name="Cosmote Sport 6 HD", country_code="gr", xmltv_id="CosmoteSport6.gr", call_sign=""),
    DLHDChannel(number="628", name="Cosmote Sport 7 HD", country_code="gr", xmltv_id="CosmoteSport7.gr", call_sign=""),
    DLHDChannel(number="629", name="Cosmote Sport 8 HD", country_code="gr", xmltv_id="CosmoteSport8.gr", call_sign=""),
    DLHDChannel(number="630", name="Cosmote Sport 9 HD", country_code="gr", xmltv_id="CosmoteSport9.gr", call_sign=""),
    DLHDChannel(number="631", name="Nova Sports 1 Greece", country_code="gr", xmltv_id="NovaSports1.gr", call_sign=""),
    DLHDChannel(number="632", name="Nova Sports 2 Greece", country_code="gr", xmltv_id="NovaSports2.gr", call_sign=""),
    DLHDChannel(number="633", name="Nova Sports 3 Greece", country_code="gr", xmltv_id="NovaSports3.gr", call_sign=""),
    DLHDChannel(number="634", name="Nova Sports 4 Greece", country_code="gr", xmltv_id="NovaSports4.gr", call_sign=""),
    DLHDChannel(number="635", name="Nova Sports 5 Greece", country_code="gr", xmltv_id="NovaSports5.gr", call_sign=""),
    DLHDChannel(number="636", name="Nova Sports 6 Greece", country_code="gr", xmltv_id="NovaSports6.gr", call_sign=""),
    DLHDChannel(
        number="637", name="Nova Sports Start Greece", country_code="gr", xmltv_id="NovaSportsStart.gr", call_sign=""
    ),
    DLHDChannel(
        number="638", name="Nova Sports Prime Greece", country_code="gr", xmltv_id="NovaSportsPrime.gr", call_sign=""
    ),
    DLHDChannel(
        number="639", name="Nova Sports News Greece", country_code="gr", xmltv_id="NovaSportsNews.gr", call_sign=""
    ),
    DLHDChannel(number="640", name="Sport1+ Germany", country_code="de", xmltv_id="Sport1Plus.de", call_sign=""),
    DLHDChannel(number="641", name="Sport1 Germany", country_code="de", xmltv_id="Sport1.de", call_sign=""),
    DLHDChannel(number="642", name="TNT Sports HD Chile", country_code="cl", xmltv_id="TNTSports1.cl", call_sign=""),
    DLHDChannel(number="643", name="FOX Deportes USA", country_code="us", xmltv_id="FoxDeportes.us", call_sign=""),
    DLHDChannel(number="644", name="TCM USA", country_code="us", xmltv_id="", call_sign="TCM"),
    DLHDChannel(number="645", name="L'Equipe France", country_code="fr", xmltv_id="LEquipe21.fr", call_sign=""),
    DLHDChannel(number="646", name="MAVTV USA", country_code="us", xmltv_id="MAVTV.us", call_sign="MAVTV"),
    DLHDChannel(number="647", name="CMT USA", country_code="us", xmltv_id="CMT.us", call_sign="CMTV"),
    DLHDChannel(number="648", name="Boomerang", country_code="us", xmltv_id="Boomerang.us", call_sign="BOOM"),
    DLHDChannel(number="649", name="Nicktoons", country_code="us", xmltv_id="Nicktoons.us", call_sign=""),
    DLHDChannel(number="650", name="TeenNick", country_code="us", xmltv_id="TeenNick.us", call_sign=""),
    DLHDChannel(
        number="651", name="Destination America", country_code="us", xmltv_id="DestinationAmerica.us", call_sign="DEST"
    ),
    DLHDChannel(number="652", name="Disney JR", country_code="us", xmltv_id="", call_sign=""),
    DLHDChannel(number="653", name="POP TV USA", country_code="us", xmltv_id="", call_sign="POPSD"),
    DLHDChannel(number="654", name="MY9TV USA", country_code="us", xmltv_id="", call_sign="WWOR"),
    DLHDChannel(number="655", name="WETV USA", country_code="us", xmltv_id="WeTV.us", call_sign="WE"),
    DLHDChannel(
        number="656", name="IFC TV USA", country_code="us", xmltv_id="IndependentFilmChannel.us", call_sign="IFC"
    ),
    DLHDChannel(number="657", name="Discovery Family", country_code="us", xmltv_id="DiscoveryFamily.us", call_sign=""),
    DLHDChannel(number="658", name="Sundance TV", country_code="us", xmltv_id="SundanceTV.us", call_sign="SUNDANC"),
    DLHDChannel(number="659", name="VICE TV", country_code="us", xmltv_id="", call_sign="VICE"),
    DLHDChannel(number="660", name="TV ONE USA", country_code="us", xmltv_id="TVOne.us", call_sign="TVONE"),
    DLHDChannel(number="661", name="Motor Trend", country_code="us", xmltv_id="MotorTrend.us", call_sign=""),
    DLHDChannel(number="662", name="METV USA", country_code="us", xmltv_id="WMEU4.us", call_sign="WJLPDT"),
    DLHDChannel(number="663", name="NHL Network USA", country_code="us", xmltv_id="NHLNetwork.us", call_sign="NHLNET"),
    DLHDChannel(number="664", name="ACC Network USA", country_code="us", xmltv_id="ACCNetwork.us", call_sign="ACC"),
    DLHDChannel(number="665", name="FYI", country_code="us", xmltv_id="FYI.us", call_sign="FYISD"),
    DLHDChannel(number="666", name="Nick Music", country_code="us", xmltv_id="NickMusic.us", call_sign=""),
    DLHDChannel(
        number="667", name="Longhorn Network USA", country_code="us", xmltv_id="LonghornNetwork.us", call_sign=""
    ),
    DLHDChannel(number="668", name="Universal Kids USA", country_code="us", xmltv_id="UniversalKids.us", call_sign=""),
    DLHDChannel(
        number="669", name="Crime+ Investigation USA", country_code="us", xmltv_id="CrimeInvestigation.us", call_sign=""
    ),
    DLHDChannel(number="670", name="S4C UK", country_code="uk", xmltv_id="S4C.uk", call_sign=""),
    DLHDChannel(
        number="671", name="Sky Cinema Premiere UK", country_code="uk", xmltv_id="SkyCinemaPremiere.uk", call_sign=""
    ),
    DLHDChannel(number="672", name="Sky Cinema Select UK", country_code="gb", xmltv_id="SkySelect.uk", call_sign=""),
    DLHDChannel(number="673", name="Sky Cinema Hits UK", country_code="uk", xmltv_id="SkyCinemaHits.uk", call_sign=""),
    DLHDChannel(
        number="674", name="Sky Cinema Greats UK", country_code="uk", xmltv_id="SkyCinemaGreats.uk", call_sign=""
    ),
    DLHDChannel(
        number="675", name="Sky Cinema Animation UK", country_code="uk", xmltv_id="SkyCinemaAnimation.uk", call_sign=""
    ),
    DLHDChannel(
        number="676", name="Sky Cinema Family UK", country_code="uk", xmltv_id="SkyCinemaFamily.uk", call_sign=""
    ),
    DLHDChannel(number="677", name="Sky Cinema Action UK", country_code="gb", xmltv_id="SkyAction.uk", call_sign=""),
    DLHDChannel(number="678", name="The Hallmark", country_code="us", xmltv_id="Hallmark.us", call_sign="HALL"),
    DLHDChannel(
        number="679", name="Sky Cinema Thriller UK", country_code="uk", xmltv_id="SkyCinemaThriller.uk", call_sign=""
    ),
    DLHDChannel(number="680", name="The Hallmark", country_code="us", xmltv_id="Hallmark.us", call_sign="HALL"),
    DLHDChannel(
        number="681",
        name="Sky Cinema Sci-Fi Horror UK",
        country_code="gb",
        xmltv_id="SkyCinemaSciFiHorror.uk",
        call_sign="",
    ),
    DLHDChannel(number="682", name="Sky Showcase UK", country_code="uk", xmltv_id="SkyShowcase.uk", call_sign=""),
    DLHDChannel(number="683", name="Sky Arts UK", country_code="uk", xmltv_id="SkyArts.uk", call_sign=""),
    DLHDChannel(number="684", name="Sky Comedy UK", country_code="uk", xmltv_id="SkyComedy.uk", call_sign=""),
    DLHDChannel(number="685", name="Showtime SHOxBET USA", country_code="us", xmltv_id="ShowtimeXBet.us", call_sign=""),
    DLHDChannel(number="686", name="Sky History", country_code="gb", xmltv_id="HistoryChannel.uk", call_sign=""),
    DLHDChannel(number="687", name="Gold UK", country_code="gb", xmltv_id="StarGold.uk", call_sign=""),
    DLHDChannel(number="688", name="Film4 UK", country_code="uk", xmltv_id="Film4.uk", call_sign=""),
    DLHDChannel(number="689", name="HBO2 USA", country_code="us", xmltv_id="HBO2.us", call_sign="HBO2"),
    DLHDChannel(number="690", name="HBO Comedy USA", country_code="us", xmltv_id="HBOComedy.us", call_sign="HBOC"),
    DLHDChannel(number="691", name="HBO Family USA", country_code="us", xmltv_id="HBOFamily.us", call_sign="HBOF"),
    DLHDChannel(number="692", name="HBO Latino USA", country_code="us", xmltv_id="HBOLatino.us", call_sign="HBOLAT"),
    DLHDChannel(
        number="693", name="HBO Signature USA", country_code="us", xmltv_id="HBOSignature.us", call_sign="HBOSIG"
    ),
    DLHDChannel(number="694", name="HBO Zone USA", country_code="us", xmltv_id="HBOZone.us", call_sign="HBOZ"),
    DLHDChannel(number="696", name="Comet USA", country_code="us", xmltv_id="Comet.us", call_sign=""),
    DLHDChannel(
        number="697", name="Cooking Channel USA", country_code="us", xmltv_id="CookingChannel.us", call_sign="COOK"
    ),
    DLHDChannel(number="698", name="TMC Channel USA", country_code="us", xmltv_id="", call_sign="TMC"),
    DLHDChannel(number="699", name="CBC CA", country_code="ca", xmltv_id="CBC.ca", call_sign=""),
    DLHDChannel(number="700", name="Tennis+ 1", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="701", name="Tennis+ 2", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="702", name="Tennis+ 3", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="703", name="Tennis+ 4", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="704", name="Tennis+ 5", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="705", name="Tennis+ 6", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="706", name="Tennis+ 7", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="707", name="Tennis+ 8", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="708", name="Tennis+ 9", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="709", name="Tennis+ 10", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="710", name="Tennis+ 11", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="711", name="Tennis+ 12", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="712", name="Tennis+ 13", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="713", name="Tennis+ 14", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="714", name="Tennis+ 15", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="715", name="Cleo TV", country_code="us", xmltv_id="CleoTV.us", call_sign="CLEO"),
    DLHDChannel(number="716", name="Sporting TV Portugal", country_code="pt", xmltv_id="SportingTV.pt", call_sign=""),
    DLHDChannel(number="717", name="AXN Movies Portugal", country_code="pt", xmltv_id="AXNMovies.pt", call_sign=""),
    DLHDChannel(number="718", name="Porto Canal Portugal", country_code="pt", xmltv_id="Porto.pt", call_sign=""),
    DLHDChannel(number="719", name="RTP 1 Portugal", country_code="pt", xmltv_id="", call_sign=""),
    DLHDChannel(number="720", name="RTP 2 Portugal", country_code="pt", xmltv_id="", call_sign=""),
    DLHDChannel(number="721", name="RTP 3 Portugal", country_code="pt", xmltv_id="", call_sign=""),
    DLHDChannel(number="722", name="SIC Portugal", country_code="pt", xmltv_id="", call_sign=""),
    DLHDChannel(number="723", name="TVI Portugal", country_code="pt", xmltv_id="", call_sign=""),
    DLHDChannel(number="724", name="TVI Reality Portugal", country_code="pt", xmltv_id="TviReality.pt", call_sign=""),
    DLHDChannel(number="725", name="Arte DE", country_code="de", xmltv_id="ARTE.de", call_sign=""),
    DLHDChannel(number="726", name="3sat DE", country_code="de", xmltv_id="3sat.de", call_sign=""),
    DLHDChannel(number="727", name="BBC 1 DE", country_code="de", xmltv_id="", call_sign=""),
    DLHDChannel(number="728", name="ZDF Info DE", country_code="de", xmltv_id="ZDFinfo.de", call_sign=""),
    DLHDChannel(number="729", name="SAT.1 DE", country_code="de", xmltv_id="Sat1.de", call_sign=""),
    DLHDChannel(number="730", name="ProSieben (PRO7) DE", country_code="de", xmltv_id="", call_sign=""),
    DLHDChannel(number="731", name="Kabel Eins (Kabel 1) DE", country_code="de", xmltv_id="Kabel1.de", call_sign=""),
    DLHDChannel(number="732", name="Sixx DE", country_code="de", xmltv_id="sixx.de", call_sign=""),
    DLHDChannel(number="733", name="MDR DE", country_code="de", xmltv_id="", call_sign=""),
    DLHDChannel(number="734", name="WDR DE", country_code="de", xmltv_id="WDR.de", call_sign=""),
    DLHDChannel(number="735", name="SWR DE", country_code="de", xmltv_id="SWR.de", call_sign=""),
    DLHDChannel(number="736", name="NDR DE", country_code="de", xmltv_id="", call_sign=""),
    DLHDChannel(number="737", name="BR Fernsehen DE", country_code="de", xmltv_id="BRFernsehenNord.de", call_sign=""),
    DLHDChannel(number="738", name="SUPER RTL DE", country_code="de", xmltv_id="SuperRTL.de", call_sign=""),
    DLHDChannel(number="739", name="SR Fernsehen DE", country_code="de", xmltv_id="SRFernsehen.de", call_sign=""),
    DLHDChannel(number="740", name="HR Fernsehen DE", country_code="de", xmltv_id="HR.de", call_sign=""),
    DLHDChannel(number="741", name="Ten Sports PK", country_code="pk", xmltv_id="", call_sign=""),
    DLHDChannel(number="742", name="AXS TV USA", country_code="us", xmltv_id="AXSTV.us", call_sign="AXSTV"),
    DLHDChannel(number="743", name="Galavisión USA", country_code="us", xmltv_id="Galavision.us", call_sign="GALA"),
    DLHDChannel(number="744", name="Fashion TV", country_code="ru", xmltv_id="FashionTV.ru", call_sign=""),
    DLHDChannel(number="745", name="Nat Geo Wild USA", country_code="us", xmltv_id="NatGeoWild.us", call_sign="NGC"),
    DLHDChannel(number="746", name="TYC Sports Argentina", country_code="ar", xmltv_id="TYCSports.ar", call_sign=""),
    DLHDChannel(number="747", name="C More Football Sweden", country_code="se", xmltv_id="", call_sign=""),
    DLHDChannel(number="748", name="COZI TV USA", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="749", name="Mundotoro TV Spain", country_code="es", xmltv_id="", call_sign=""),
    DLHDChannel(number="750", name="C SPAN 1", country_code="us", xmltv_id="CSPAN.us", call_sign="CSPAN"),
    DLHDChannel(
        number="751",
        name="FETV - Family Entertainment Television",
        country_code="us",
        xmltv_id="FamilyFriendlyEntertainment.us",
        call_sign="FETV",
    ),
    DLHDChannel(number="752", name="Grit Channel", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(
        number="753", name="NBC Sports Bay Area", country_code="us", xmltv_id="NBCSportsBayArea.us", call_sign=""
    ),
    DLHDChannel(number="754", name="NBC Sports Boston", country_code="us", xmltv_id="SportsBoston.us", call_sign=""),
    DLHDChannel(
        number="755", name="NBC Sports California", country_code="us", xmltv_id="NBCSportsCalifornia.us", call_sign=""
    ),
    DLHDChannel(number="756", name="FOX Soccer Plus", country_code="us", xmltv_id="FoxSoccerPlus.us", call_sign=""),
    DLHDChannel(number="757", name="Fight Network", country_code="ca", xmltv_id="FightNetwork.ca", call_sign=""),
    DLHDChannel(number="758", name="Fox Sports 2 USA", country_code="us", xmltv_id="FoxSports2.us", call_sign=""),
    DLHDChannel(number="759", name="SportsNet New York (SNY)", country_code="us", xmltv_id="", call_sign="SNY"),
    DLHDChannel(number="760", name="Globo SP", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="761", name="Globo RIO", country_code="br", xmltv_id="GloboRJ.br", call_sign=""),
    DLHDChannel(number="762", name="NESN USA", country_code="us", xmltv_id="NewEnglandSportsNetwork.us", call_sign=""),
    DLHDChannel(number="763", name="YES Network USA", country_code="us", xmltv_id="YESNetwork.us", call_sign="YES"),
    DLHDChannel(
        number="764", name="Spectrum Sportsnet LA", country_code="us", xmltv_id="SpectrumSportsNetLA.us", call_sign=""
    ),
    DLHDChannel(number="765", name="MSG USA", country_code="us", xmltv_id="MadisonSquareGarden.us", call_sign="MSG"),
    DLHDChannel(number="766", name="ABCNY USA", country_code="us", xmltv_id="WABC.us", call_sign="ABC"),
    DLHDChannel(number="767", name="Fox Sports Argentina", country_code="ar", xmltv_id="FoxSports.ar", call_sign=""),
    DLHDChannel(number="768", name="FOXNY USA", country_code="us", xmltv_id="WNYW.us", call_sign="WNYW"),
    DLHDChannel(number="769", name="NBCNY USA", country_code="us", xmltv_id="WNBC.us", call_sign="WNBC"),
    DLHDChannel(
        number="770", name="Marquee Sports Network", country_code="", xmltv_id="MarqueeSportsNetwork.us", call_sign=""
    ),
    DLHDChannel(number="771", name="New! CWPIX 11", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(
        number="775", name="Fox Weather Channel", country_code="us", xmltv_id="FoxWeather.us", call_sign="FOXWX"
    ),
    DLHDChannel(
        number="776", name="NBC Sports Chicago", country_code="us", xmltv_id="NBCSportsChicago.us", call_sign=""
    ),
    DLHDChannel(
        number="777",
        name="NBC Sports Philadelphia",
        country_code="us",
        xmltv_id="NBCSportsPhiladelphia.us",
        call_sign="",
    ),
    DLHDChannel(
        number="778", name="NBC Sports Washington", country_code="us", xmltv_id="NBCSportsWashington.us", call_sign=""
    ),
    DLHDChannel(number="779", name="Max Sport 1 Croatia", country_code="hr", xmltv_id="MAXSport1.hr", call_sign=""),
    DLHDChannel(number="780", name="Max Sport 2 Croatia", country_code="hr", xmltv_id="MAXSport2.hr", call_sign=""),
    DLHDChannel(number="781", name="Alkass One", country_code="qa", xmltv_id="AlKass.qa", call_sign=""),
    DLHDChannel(number="782", name="Alkass Two", country_code="qa", xmltv_id="", call_sign=""),
    DLHDChannel(number="783", name="Alkass Three", country_code="qa", xmltv_id="", call_sign=""),
    DLHDChannel(number="784", name="Alkass Four", country_code="qa", xmltv_id="", call_sign=""),
    DLHDChannel(number="785", name="ABS-CBN", country_code="ph", xmltv_id="ANC.ph", call_sign=""),
    DLHDChannel(number="786", name="DSTV Mzansi Magic", country_code="za", xmltv_id="MzansiMagic.za", call_sign=""),
    DLHDChannel(number="788", name="Fox Sports 2 Argentina", country_code="ar", xmltv_id="FoxSports2.ar", call_sign=""),
    DLHDChannel(number="789", name="Fox Sports 3 Argentina", country_code="ar", xmltv_id="FoxSports3.ar", call_sign=""),
    DLHDChannel(number="800", name="6'eren Denmark", country_code="dk", xmltv_id="6eren.dk", call_sign=""),
    DLHDChannel(number="801", name="DR1 Denmark", country_code="dk", xmltv_id="DR1.dk", call_sign=""),
    DLHDChannel(number="802", name="DR2 Denmark", country_code="dk", xmltv_id="DR2.dk", call_sign=""),
    DLHDChannel(number="803", name="Kanal 4 Denmark", country_code="dk", xmltv_id="Kanal4.dk", call_sign=""),
    DLHDChannel(number="804", name="Kanal 5 Denmark", country_code="dk", xmltv_id="Kanal5.dk", call_sign=""),
    DLHDChannel(number="805", name="CANAL9 Denmark", country_code="dk", xmltv_id="", call_sign=""),
    DLHDChannel(number="806", name="MTV Denmark", country_code="dk", xmltv_id="MTV.dk", call_sign=""),
    DLHDChannel(number="807", name="TV2 Bornholm Denmark", country_code="dk", xmltv_id="TV2Bornholm.dk", call_sign=""),
    DLHDChannel(number="808", name="TV2 Sport X Denmark", country_code="dk", xmltv_id="TV2SportX.dk", call_sign=""),
    DLHDChannel(number="809", name="TV3 Sport Denmark", country_code="dk", xmltv_id="TV3Sport.dk", call_sign=""),
    DLHDChannel(number="810", name="TV2 Sport Denmark", country_code="dk", xmltv_id="TV2Sport.dk", call_sign=""),
    DLHDChannel(number="812", name="C More First Sweden", country_code="no", xmltv_id="CMoreFirst.no", call_sign=""),
    DLHDChannel(number="813", name="C More Hits Sweden", country_code="no", xmltv_id="CMoreHits.no", call_sign=""),
    DLHDChannel(number="814", name="C More Series Sweden", country_code="no", xmltv_id="CMoreSeries.no", call_sign=""),
    DLHDChannel(
        number="815", name="V Film Premiere", country_code="no", xmltv_id="ViasatFilmPremiere.no", call_sign=""
    ),
    DLHDChannel(number="816", name="V Film Family", country_code="no", xmltv_id="ViasatFilmFamily.no", call_sign=""),
    DLHDChannel(number="817", name="TV2 Denmark", country_code="dk", xmltv_id="TV2.dk", call_sign=""),
    DLHDChannel(number="818", name="TV2 Zulu", country_code="za", xmltv_id="", call_sign=""),
    DLHDChannel(number="819", name="TV3+ Denmark", country_code="dk", xmltv_id="TV3Plus.dk", call_sign=""),
    DLHDChannel(number="820", name="FOX Sports 502 AU", country_code="au", xmltv_id="", call_sign=""),
    DLHDChannel(number="821", name="FOX Sports 503 AU", country_code="au", xmltv_id="FoxSports3.au", call_sign=""),
    DLHDChannel(number="822", name="FOX Sports 504 AU", country_code="au", xmltv_id="", call_sign=""),
    DLHDChannel(number="823", name="FOX Sports 505 AU", country_code="au", xmltv_id="FoxSports5.au", call_sign=""),
    DLHDChannel(number="824", name="FOX Sports 506 AU", country_code="au", xmltv_id="FoxSports6.au", call_sign=""),
    DLHDChannel(number="825", name="FOX Sports 507 AU", country_code="au", xmltv_id="", call_sign=""),
    DLHDChannel(
        number="826", name="Liverpool TV (LFC TV)", country_code="gb", xmltv_id="LiverpoolFCTV.uk", call_sign=""
    ),
    DLHDChannel(number="827", name="DSTV M-Net", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="828", name="DSTV kykNET & kie", country_code="za", xmltv_id="kykNETKie.za", call_sign=""),
    DLHDChannel(number="829", name="MASN USA", country_code="us", xmltv_id="MASN.us", call_sign=""),
    DLHDChannel(number="830", name="Fox Sports Premium MX", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="831", name="Citytv", country_code="", xmltv_id="", call_sign=""),
    DLHDChannel(number="832", name="CBC CA", country_code="ca", xmltv_id="CBC.ca", call_sign=""),
    DLHDChannel(number="833", name="TVA Sports", country_code="ca", xmltv_id="TVASports.ca", call_sign=""),
    DLHDChannel(number="834", name="TVA Sports 2", country_code="ca", xmltv_id="TVASports2.ca", call_sign=""),
    DLHDChannel(number="835", name="Noovo CA", country_code="ca", xmltv_id="Noovo.ca", call_sign=""),
    DLHDChannel(number="836", name="Global CA", country_code="ca", xmltv_id="Global.ca", call_sign=""),
    DLHDChannel(number="837", name="Yes TV CA", country_code="ca", xmltv_id="CITS.ca", call_sign=""),
    DLHDChannel(number="838", name="CTV 2 Canada", country_code="cn", xmltv_id="CCTV2.cn", call_sign=""),
    DLHDChannel(number="839", name="RDS CA", country_code="ca", xmltv_id="RDS.ca", call_sign=""),
    DLHDChannel(number="840", name="RDS 2 CA", country_code="ca", xmltv_id="RDS2.ca", call_sign=""),
    DLHDChannel(number="841", name="RDS Info CA", country_code="ca", xmltv_id="RDSInfo.ca", call_sign=""),
    DLHDChannel(number="842", name="TVO CA", country_code="ca", xmltv_id="", call_sign=""),
    DLHDChannel(number="850", name="Rai 1 Italy", country_code="it", xmltv_id="RaiUno.it", call_sign=""),
    DLHDChannel(number="850", name="Rai 1 Italy", country_code="it", xmltv_id="RaiUno.it", call_sign=""),
    DLHDChannel(number="851", name="Rai 2 Italy", country_code="it", xmltv_id="RaiDue.it", call_sign=""),
    DLHDChannel(number="852", name="Rai 3 Italy", country_code="it", xmltv_id="RaiTre.it", call_sign=""),
    DLHDChannel(number="853", name="Rai 3 Italy", country_code="it", xmltv_id="RaiTre.it", call_sign=""),
    DLHDChannel(number="854", name="Italia 1 Italy", country_code="it", xmltv_id="Italia1.it", call_sign=""),
    DLHDChannel(number="855", name="La7 Italy", country_code="it", xmltv_id="La7.it", call_sign=""),
    DLHDChannel(number="856", name="LA7d HD+ Italy", country_code="it", xmltv_id="", call_sign=""),
    DLHDChannel(number="857", name="20 Mediaset Italy", country_code="it", xmltv_id="20Mediaset.it", call_sign=""),
    DLHDChannel(number="858", name="Rai Premium Italy", country_code="it", xmltv_id="RaiPremium.it", call_sign=""),
    DLHDChannel(
        number="859",
        name="Sky Cinema Collection Italy",
        country_code="it",
        xmltv_id="SkyCinemaCollection.it",
        call_sign="",
    ),
    DLHDChannel(number="860", name="Sky Cinema Uno Italy", country_code="it", xmltv_id="SkyCinemaUno.it", call_sign=""),
    DLHDChannel(
        number="861", name="Sky Cinema Action Italy", country_code="it", xmltv_id="SkyCinemaAction.it", call_sign=""
    ),
    DLHDChannel(
        number="862", name="8Sky Cinema Comedy Italy", country_code="it", xmltv_id="SkyCinemaComedy.it", call_sign=""
    ),
    DLHDChannel(
        number="863", name="Sky Cinema Uno +24 Italy", country_code="it", xmltv_id="SkyCinemaPlus24.it", call_sign=""
    ),
    DLHDChannel(
        number="864", name="Sky Cinema Romance Italy", country_code="it", xmltv_id="SkyCinemaRomance.it", call_sign=""
    ),
    DLHDChannel(
        number="865", name="Sky Cinema Family Italy", country_code="it", xmltv_id="SkyCinemaFamily.it", call_sign=""
    ),
    DLHDChannel(
        number="866", name="Sky Cinema Due +24 Italy", country_code="it", xmltv_id="SkyCinemaDuePlus24.it", call_sign=""
    ),
    DLHDChannel(
        number="867", name="Sky Cinema Drama Italy", country_code="it", xmltv_id="SkyCinemaDrama.it", call_sign=""
    ),
    DLHDChannel(
        number="868",
        name="8Sky Cinema Suspense Italy",
        country_code="it",
        xmltv_id="SkyCinemaSuspense.it",
        call_sign="",
    ),
    DLHDChannel(number="869", name="Sky Sport 24 Italy", country_code="it", xmltv_id="SkySport24.it", call_sign=""),
    DLHDChannel(
        number="870", name="Sky Sport Calcio Italy", country_code="it", xmltv_id="SkySportCalcio.it", call_sign=""
    ),
    DLHDChannel(number="871", name="Sky Calcio 1 (251) Italy", country_code="it", xmltv_id="", call_sign=""),
    DLHDChannel(number="872", name="Sky Calcio 2 (252) Italy", country_code="it", xmltv_id="", call_sign=""),
    DLHDChannel(number="873", name="Sky Calcio 3 (253) Italy", country_code="it", xmltv_id="", call_sign=""),
    DLHDChannel(number="874", name="Sky Calcio 4 (254) Italy", country_code="it", xmltv_id="", call_sign=""),
    DLHDChannel(number="875", name="Sky Calcio 5 (255) Italy", country_code="it", xmltv_id="", call_sign=""),
    DLHDChannel(number="876", name="Sky Calcio 6 (256) Italy", country_code="it", xmltv_id="", call_sign=""),
    DLHDChannel(number="877", name="Sky Calcio 7 (257) Italy", country_code="it", xmltv_id="", call_sign=""),
    DLHDChannel(number="878", name="EuroSport 1 Italy", country_code="il", xmltv_id="Eurosport1.il", call_sign=""),
    DLHDChannel(number="879", name="EuroSport 2 Italy", country_code="it", xmltv_id="Eurosport2.it", call_sign=""),
    DLHDChannel(number="880", name="Sky Serie Italy", country_code="it", xmltv_id="SkySerie.it", call_sign=""),
    DLHDChannel(number="881", name="Sky UNO Italy", country_code="it", xmltv_id="SkyUno.it", call_sign=""),
    DLHDChannel(number="882", name="Rai Sport Italy", country_code="it", xmltv_id="RaiSport.it", call_sign=""),
    DLHDChannel(number="8111", name="C More Stars Sweden", country_code="no", xmltv_id="CMoreStars.no", call_sign=""),
]


def get_channels() -> Iterator[DLHDChannel]:
    for channel in _CHANNELS:
        if config.CHANNEL_ALLOW is not None:
            if channel.number not in config.CHANNEL_ALLOW:
                continue
        if config.CHANNEL_EXCLUDE is not None:
            if channel.number in config.CHANNEL_EXCLUDE:
                continue

        if config.COUNTRY_ALLOW is not None:
            if channel.country_code not in config.COUNTRY_ALLOW:
                continue

        if config.COUNTRY_EXCLUDE is not None:
            if channel.country_code in config.COUNTRY_EXCLUDE:
                continue

        yield channel
