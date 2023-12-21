from typing import cast
import urllib.parse
from xml.sax import saxutils

import httpx
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response, StreamingResponse

from dlhdhr import config
from dlhdhr.dlhd import DLHDClient
from dlhdhr.tuner import TunerManager, TunerNotFoundError


def get_public_url(request: Request, path: str) -> str:
    return urllib.parse.urljoin(str(request.url), path)


async def channel_playlist_m3u8(request: Request) -> Response:
    channel_number: str = str(request.path_params["channel_number"])

    dlhd = cast(DLHDClient, request.app.state.dlhd)
    channel = await dlhd.get_channel(channel_number)
    if not channel:
        return Response("", status_code=404)

    playlist = await dlhd.get_channel_playlist(channel)
    return Response(content=playlist.dumps(), status_code=200, media_type="application/vnd.apple.mpegurl")


async def channel_segment_ts(request: Request) -> Response:
    channel_number: str = str(request.path_params["channel_number"])
    segment_path: str = f"{request.path_params['segment_path']}.ts"

    dlhd = cast(DLHDClient, request.app.state.dlhd)

    dlhd = cast(DLHDClient, request.app.state.dlhd)
    channel = await dlhd.get_channel(channel_number)
    if not channel:
        return Response("", status_code=404)

    return StreamingResponse(
        dlhd.stream_segment(channel, segment_path),
        status_code=200,
        media_type="video/mp2t",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Content-Disposition": "inline",
            "Content-Transfer-Enconding": "binary",
        },
    )


async def channel_proxy(request: Request) -> Response:
    channel_number: str = str(request.path_params["channel_number"])

    dlhd = cast(DLHDClient, request.app.state.dlhd)

    channel = await dlhd.get_channel(channel_number)
    if not channel:
        return Response("", status_code=404)

    tuners = cast(TunerManager, request.app.state.tuners)

    try:
        tuner = tuners.claim_tuner(channel)
    except TunerNotFoundError:
        return Response("", status_code=404)

    listener = await tuner.get_listener()

    async def _generator():
        async for chunk in listener:
            yield chunk

    return StreamingResponse(
        _generator(),
        status_code=200,
        media_type="video/mp2t",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Content-Disposition": "inline",
            "Content-Transfer-Enconding": "binary",
        },
    )


async def listings_json(request: Request) -> JSONResponse:
    dlhd = cast(DLHDClient, request.app.state.dlhd)
    channels = sorted(await dlhd.get_channels(), key=lambda c: int(c.number))
    return JSONResponse(
        [
            {
                "GuideName": channel.name,
                "GuideNumber": channel.number,
                "URL": get_public_url(request, channel.channel_proxy),
            }
            for channel in channels
        ]
    )


async def discover_json(request: Request) -> JSONResponse:
    tuners = cast(TunerManager, request.app.state.tuners)

    return JSONResponse(
        {
            "FriendlyName": "dlhdhomerun",
            "Manufacturer": "dlhdhomerun - Silicondust",
            "ManufacturerURL": "https://c653labs.com/",
            "ModelNumber": "HDTC-2US",
            "FirmwareName": "hdhomeruntc_atsc",
            "TunerCount": tuners.total_available_listeners,
            "FirmwareVersion": "20170930",
            "DeviceID": "dlhdhomerun",
            "DeviceAuth": "",
            "BaseURL": get_public_url(request, "/"),
            "LineupURL": get_public_url(request, "/lineup.json"),
        }
    )


async def lineup_status_json(_: Request) -> JSONResponse:
    return JSONResponse(
        {
            "ScanInProgress": 0,
            "ScanPossible": 1,
            "Source": "Cable",
            "SourceList": ["Cable"],
        }
    )


async def xmltv_xml(request: Request) -> Response:
    if config.EPG_PROVIDER == "epg.best":
        if not config.EPG_BEST_XMLTV_URL:
            return Response("", status_code=404)

        async def _generator():
            if not config.EPG_BEST_XMLTV_URL:
                return

            async with httpx.AsyncClient() as client:
                async with client.stream("GET", config.EPG_BEST_XMLTV_URL) as res:
                    async for chunk in res.aiter_bytes():
                        yield chunk

        headers = {}
        if config.EPG_BEST_XMLTV_URL.endswith(".gz"):
            headers["Content-Encoding"] = "gzip"

        return StreamingResponse(
            _generator(),
            status_code=200,
            media_type="application/xml; charset=utf-8",
            headers={
                "Content-Encoding": "gzip",
            },
        )

    dlhd = cast(DLHDClient, request.app.state.dlhd)

    dlhd_channels = await dlhd.get_channels()

    response = '<tv generator-info-name="dlhdhr">'

    for channel in dlhd_channels:
        name = saxutils.escape(channel.name)
        response += f'<channel id="{channel.number}">'
        response += f'<display-name lang="en">{name}</display-name>'
        response += f"<lcn>{channel.number}</lcn>"
        response += "</channel>"
    response += "</tv>"

    return Response(response, media_type="application/xml; charset=utf-8")


async def iptv_m3u(request: Request) -> Response:
    dlhd = cast(DLHDClient, request.app.state.dlhd)
    dlhd_channels = await dlhd.get_channels()

    output = "#EXTM3U\n"
    for channel in dlhd_channels:
        if not channel.tvg_id:
            continue
        output += f'#EXTINF:-1 CUID="{channel.number}" tvg-id="{channel.tvg_id}" tvg-chno="{channel.number}" channel-id="{channel.number}",{channel.name}\n'
        output += get_public_url(request, channel.channel_proxy)
        output += "\n"

    return Response(output, media_type="text/plain")


def create_app() -> Starlette:
    dlhd_client = DLHDClient()
    tuner_manager = TunerManager()

    app = Starlette()
    app.state.dlhd = dlhd_client
    app.state.tuners = tuner_manager
    app.add_route("/discover.json", discover_json)
    app.add_route("/lineup_status.json", lineup_status_json)
    app.add_route("/listings.json", listings_json)
    app.add_route("/lineup.json", listings_json)
    app.add_route("/xmltv.xml", xmltv_xml)
    app.add_route("/iptv.m3u", iptv_m3u)
    app.add_route("/channel/{channel_number:int}/playlist.m3u8", channel_playlist_m3u8)
    app.add_route("/channel/{channel_number:int}/{segment_path:path}.ts", channel_segment_ts)
    app.add_route("/channel/{channel_number:int}", channel_proxy)

    return app
