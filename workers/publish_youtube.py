import os
import tempfile

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from utils.video_selector import (
    get_processed_video_for_platform,
    get_random_unprocessed_video
)

from utils.video_status import (
    mark_uploaded,
    mark_upload_failed
)

from processing.process_video import (
    process_video
)

from drive.drive_utils import (
    download_file
)

from youtube.generate_metadata import (
    generate_youtube_metadata
)

from youtube.youtube_upload import (
    upload_youtube_video
)

PLATFORM = "youtube"


# Select video 

def get_video():

    # Priority 1:
    # Already processed video waiting for YouTube

    video = get_processed_video_for_platform(
        PLATFORM
    )

    if video:

        print(
            f"Found processed video {video['id']}"
        )

        return video

    # Priority 2:
    # Process a new source video

    source_video = (
        get_random_unprocessed_video()
    )

    if not source_video:

        raise Exception(
            "No videos available"
        )

    print(
        f"Processing source video {source_video['id']}"
    )

    process_video(
        source_video
    )

    # Reload

    video = get_processed_video_for_platform(
        PLATFORM
    )

    if not video:

        raise Exception(
            "Processing failed"
        )

    return video


# Download Processed Video

def download_processed_video(
    video,
    output_path
):

    download_file(
        video["processed"]["drive_file_id"],
        output_path
    )


# Main Publish Logic

def main():

    video = get_video()

    try:

        analysis = (
            video["processed"]["analysis"]
        )

        print(
            "Generating YouTube metadata..."
        )

        metadata = (
            generate_youtube_metadata(
                analysis
            )
        )

        with tempfile.TemporaryDirectory() as temp_dir:

            video_path = os.path.join(
                temp_dir,
                "video.mp4"
            )

            print(
                "Downloading processed video..."
            )

            download_processed_video(
                video,
                video_path
            )

            print(
                "Uploading to YouTube..."
            )

            upload_id = (
                upload_youtube_video(
                    video_path=video_path,
                    title=metadata["title"],
                    description=metadata["description"],
                    tags=metadata.get(
                        "tags",
                        []
                    )
                )
            )

        mark_uploaded(
            video_id=video["id"],
            platform=PLATFORM,
            upload_id=upload_id
        )

        print(
            f"Upload successful: {upload_id}"
        )

    except Exception as e:

        mark_upload_failed(
            video_id=video["id"],
            platform=PLATFORM,
            error=str(e)
        )

        raise


# EntryPoint 

if __name__ == "__main__":
    main()
