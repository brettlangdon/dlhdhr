# DLHDHomeRun

[![PyPI - Version](https://img.shields.io/pypi/v/dlhdhr.svg)](https://pypi.org/project/dlhdhr
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dlhdhr.svg)](https://pypi.org/project/dlhdhr

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

### pip

```console
pip install dlhdhr
```

### docker

``` console
docker run --rm -p 8000:8000 brettlangdon/dlhdhr:latest
```

## Running

``` console
# Start the server
dlhdhr
```

## Configuration

All Configuration is done via environment variables.

``` console
DLHDHR_HOST="0.0.0.0" DLHDHR_PORT="8080" dlhdhr

docker run --rm -e "DLHDHR_PORT=8080" -p 8080:8080 brettlangdon/dlhdhr:latest
```

### Server

- `DLHDHR_HOST="<ip-address>"`
  - Which ip address bind to. `dlhdhr` command default is "127.0.0.1", the docker container defaults to "0.0.0.0".
- `DLHDHR_PORT="<port>"`
  - Which port the server should bind to. Default is "8000".

### Channel selection
By default `dlhdhr` will include all channels from DaddyLive, however you can select or exclude specific channels.

- `DLHDHR_CHANNEL_EXCLUDE="<cn>,<cn>,<cn>,...`
  - Exclude the specified DaddyLive channel numbers.
- `DLHDHR_CHANNEL_ALLOW="<cn>,<cn>,<cn>,...`
  - Include only the specified DaddyLive channel numbers.

### EPG
#### default

By default `dlhdhr` will generate an `xmltv.xml` with only the channel numbers and names.

#### epg.best
- `DLHDHR_EPG_PROVIDER="epg.best"`
- `DLHDHR_EPG_BEST_XMLTV_URL="https://epg.best/<filename>.m3u"`

## Endpoints

- `/discover.json`
- `/lineup_status.json`
- `/listings.json`
- `/lineup.json`
- `/xmltv.xml`
- `/iptv.m3u`
- `/channel/{channel_number:int}/playlist.m3u8`
- `/channel/{channel_number:int}/{segment_path:path}.ts`
- `/channel/{channel_number:int}`

## License

`dlhdhr` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
