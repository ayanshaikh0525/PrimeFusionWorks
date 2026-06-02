from youtube.youtube_upload import (
    upload_youtube_video
)

video_id = upload_youtube_video(
    video_path="sample.mp4",
    title="Test Upload",
    description="Uploaded via API",
    tags=[
        "test",
        "shorts"
    ]
)

print(video_id)
