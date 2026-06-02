from datetime import datetime

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from utils.json_utils import (
    load_videos,
    save_videos
)




def now():
    return datetime.utcnow().isoformat()


# Helper

def _get_video(videos, video_id):

    for video in videos:

        if video["id"] == video_id:
            return video

    raise ValueError(
        f"Video {video_id} not found"
    )


# mark_processing_started

def mark_processing_started(
    video_id
):

    videos = load_videos()

    video = _get_video(
        videos,
        video_id
    )

    video.setdefault(
        "workflow",
        {}
    )

    video["workflow"]["processing_started"] = now()

    save_videos(videos)


# mark_processing_completed

def mark_processing_completed(
    video_id,
    processed_file_id,
    processed_link,
    analysis
):

    videos = load_videos()

    video = _get_video(
        videos,
        video_id
    )

    video["processed"] = {
        "exists": True,
        "drive_file_id": processed_file_id,
        "drive_link": processed_link,
        "analysis": analysis
    }

    video.setdefault(
        "workflow",
        {}
    )

    video["workflow"][
        "processing_completed"
    ] = now()

    save_videos(videos)


# mark_source_deleted

def mark_source_deleted(
    video_id
):

    videos = load_videos()

    video = _get_video(
        videos,
        video_id
    )

    video["source"]["deleted"] = True

    video.setdefault(
        "workflow",
        {}
    )

    video["workflow"][
        "source_deleted"
    ] = now()

    save_videos(videos)


# mark_uploaded

def mark_uploaded(
    video_id,
    platform,
    upload_id
):

    videos = load_videos()

    video = _get_video(
        videos,
        video_id
    )

    video["platforms"][platform] = {
        "uploaded": True,
        "upload_id": upload_id,
        "uploaded_at": now(),
        "attempts": 0,
        "last_error": ""
    }

    save_videos(videos)


# mark_upload_failed

def mark_upload_failed(
    video_id,
    platform,
    error
):

    videos = load_videos()

    video = _get_video(
        videos,
        video_id
    )

    platform_data = video[
        "platforms"
    ][platform]

    platform_data["attempts"] = (
        platform_data.get(
            "attempts",
            0
        ) + 1
    )

    platform_data[
        "last_error"
    ] = str(error)

    save_videos(videos)


# mark_metadata_generated

def mark_metadata_generated(
    video_id,
    platform,
    metadata
):

    videos = load_videos()

    video = _get_video(
        videos,
        video_id
    )

    video["platforms"][
        platform
    ]["metadata"] = metadata

    save_videos(videos)
