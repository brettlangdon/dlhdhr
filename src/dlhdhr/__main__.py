import uvicorn

from dlhdhr import config
from dlhdhr.app import create_app


def main() -> None:
    app = create_app()
    uvicorn.run(app, host=config.HOST, port=config.PORT)


if __name__ == "__main__":
    main()
