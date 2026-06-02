
import os
import tempfile

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from drive.drive_utils import (
    download_file,
    upload_file,
    delete_file,
    get_drive_link
)

from processing.extract_keyframes import extract_keyframes
from processing.analyze_video import analyze_video_frames
from processing.watermark_video import add_watermark
from utils.video_status import *

from utils.json_utils import (
    load_videos,
    save_videos
)

from config.settings import (
    PROCESSED_FOLDER_ID
)


WATERMARK_PATH = ROOT / "assets" / "watermark.png"


def process_video(video_record):

    source_file_id = video_record["source"]["drive_file_id"]

    with tempfile.TemporaryDirectory() as temp_dir:

        original_video = os.path.join(
            temp_dir,
            "source.mp4"
        )

        watermarked_video = os.path.join(
            temp_dir,
            "processed.mp4"
        )

        print("Downloading source video...")

        download_file(
            source_file_id,
            original_video
        )

        print("Extracting frames...")

        frames = extract_keyframes(
            original_video,
            output_dir=os.path.join(
                temp_dir,
                "frames"
            ),
            num_frames=10
        )

        print("Analyzing video...")

        analysis = analyze_video_frames(
            frames
        )

        print("Adding watermark...")

        add_watermark(
            original_video,
            WATERMARK_PATH,
            watermarked_video
        )

        print("Uploading processed video...")

        processed_file_id = upload_file(
            watermarked_video,
            PROCESSED_FOLDER_ID
        )

        processed_link = get_drive_link(
            processed_file_id
        )

        print("Deleting source video...")

        delete_file(
            source_file_id
        )

        mark_processing_completed(
            video_id=video_record["id"],
            processed_file_id=processed_file_id,
            processed_link=processed_link,
            analysis=analysis
        )
        
        mark_source_deleted(
            video_record["id"]
        )

        return {
            "processed_file_id": processed_file_id,
            "processed_link": processed_link,
            "analysis": analysis
        }




def update_video_record(
    video_id,
    processed_file_id,
    processed_link,
    analysis
):

    videos = load_videos()

    for video in videos:

        if video["id"] == video_id:

            video["source"]["deleted"] = True

            video["processed"] = {
                "exists": True,
                "drive_file_id": processed_file_id,
                "drive_link": processed_link,
                "analysis": analysis
            }

            break

    save_videos(videos)
