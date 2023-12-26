import uvicorn

from dlhdhr import config
from dlhdhr.app import create_app


def main() -> None:
    print("== CONFIG ==")
    for name, value in vars(config).items():
        if name.islower():
            continue
        print(f"{name}: {value}")
    print("====")

    app = create_app()
    uvicorn.run(app, host=config.HOST, port=config.PORT)


if __name__ == "__main__":
    main()
