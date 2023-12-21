import uvicorn

from dlhdhr import config
from dlhdhr.app import create_app


def main() -> None:
    print("== CONFIG ==")
    print(f"HOST: {config.HOST}")
    print(f"PORT: {config.PORT}")
    print(f"CHANNEL_EXCLUDE: {config.CHANNEL_EXCLUDE}")
    print(f"CHANNEL_ALLOW: {config.CHANNEL_ALLOW}")
    print(f"EPG_PROVIDER: {config.EPG_PROVIDER}")
    if config.EPG_PROVIDER == "epg.best":
        print(f"EPG_BEST_XMLTV_URL: {config.EPG_BEST_XMLTV_URL}")
    print("====")

    app = create_app()
    uvicorn.run(app, host=config.HOST, port=config.PORT)


if __name__ == "__main__":
    main()
