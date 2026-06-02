
import os
import tempfile

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from drive.drive_utils import (
    download_file,
    upload_file,
    get_drive_link
)

from processing.extract_keyframes import extract_keyframes
from processing.analyze_video import analyze_video_frames
from utils.video_status import *

from utils.json_utils import (
    load_videos,
    save_videos
)




def process_video(video_record):

    source_file_id = video_record["source"]["drive_file_id"]

    with tempfile.TemporaryDirectory() as temp_dir:

        original_video = os.path.join(
            temp_dir,
            "source.mp4"
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

        mark_processing_completed(
            video_id=video_record["id"],
            analysis=analysis
        )
        

        return {
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
