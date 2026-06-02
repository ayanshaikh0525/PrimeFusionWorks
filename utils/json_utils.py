import json

from config.settings import MASTER_JSON_PATH


def load_videos():

    with open(
        MASTER_JSON_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def save_videos(data):

    with open(
        MASTER_JSON_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )
