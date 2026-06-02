import os
import subprocess

# watermark_path = "assets/watermark.png"

def add_watermark(
    video_path,
    watermark_path,
    output_path
):
    """
    Adds watermark to video.

    Top-right corner.
    Slight margin.
    Scaled watermark.
    """

    cmd = [
        "ffmpeg",
        "-y",

        "-i",
        video_path,

        "-i",
        watermark_path,

        "-filter_complex",
        (
            "[1:v]"
            "scale=130:-1[wm];"
            "[0:v][wm]"
            "overlay=W-w-22:10"
        ),

        "-codec:a",
        "copy",

        output_path
    ]

    subprocess.run(
        cmd,
        check=True
    )

    return output_path
