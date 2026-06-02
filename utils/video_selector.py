import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from utils.json_utils import load_videos


def get_processed_video_for_platform(
    platform
):
    videos = load_videos()

    candidates = []

    for video in videos:

        if (
            video["processed"]["exists"]
            and not video["platforms"][platform]["uploaded"]
        ):
            candidates.append(video)

    if not candidates:
        return None

    return candidates[0]



def get_random_unprocessed_video():

    videos = load_videos()

    candidates = []

    for video in videos:

        if not video["processed"]["exists"]:
            candidates.append(video)

    if not candidates:
        return None

    return random.choice(
        candidates
    )



def get_video_for_platform(
    platform
):

    processed_video = (
        get_processed_video_for_platform(
            platform
        )
    )

    if processed_video:
        return processed_video

    return None


# Find Videos Needing Processing

def count_unprocessed_videos():

    videos = load_videos()

    return len([
        v
        for v in videos
        if not v["processed"]["exists"]
    ])



# Find Pending Uploads

def count_pending_uploads(
    platform
):
    videos = load_videos()

    return len([
        v
        for v in videos
        if (
            v["processed"]["exists"]
            and not v["platforms"][platform]["uploaded"]
        )
    ])
