import os
import json

import google.generativeai as genai


genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


MODEL = genai.GenerativeModel(
    "gemini-2.5-flash"
)


PROMPT = """
Analyze these video frames.

Return JSON only.

{
  "category": "",
  "project": "",
  "summary": "",
  "materials": [],
  "tools": [],
  "viral_hook": ""
}
"""


def analyze_video_frames(
    frame_paths
):

    images = []

    for path in frame_paths:

        with open(path, "rb") as f:

            images.append(
                {
                    "mime_type": "image/jpeg",
                    "data": f.read()
                }
            )

    response = MODEL.generate_content(
        [PROMPT] + images
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        ).strip()

    return json.loads(text)