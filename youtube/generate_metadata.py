# generate youtube metadata 
import json
import os
import re

import google.generativeai as genai

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-3.1-flash-lite"
)


PROMPT = """
You are a world-class YouTube Shorts growth strategist, viral content expert, and YouTube SEO specialist.

Your objective is to maximize:

- Click Through Rate (CTR)
- Average View Duration (AVD)
- Audience Retention
- Rewatches
- Shares
- Comments
- Subscriber Conversion
- YouTube Recommendation Distribution

You will receive a structured analysis of a video.

Using the analysis, generate metadata optimized specifically for YouTube Shorts.

TITLE REQUIREMENTS:
- Maximum 100 characters
- Create strong curiosity gaps
- Use proven viral copywriting techniques
- Focus on the most surprising, impressive, emotional, satisfying, shocking, or useful moment
- Avoid clickbait that is not supported by the video
- Prioritize watch intent and CTR
- Make the title feel impossible to ignore
- Use natural language, not keyword stuffing

DESCRIPTION REQUIREMENTS:
- First 2 lines must hook viewers immediately
- Explain what happens in the video
- Include primary SEO keywords naturally
- Include related search terms naturally
- Encourage comments and engagement
- Optimize for YouTube search and recommendations
- Keep concise and readable

TAG REQUIREMENTS:
- Generate 15-25 highly relevant tags
- Include broad niche keywords
- Include specific topic keywords
- Include search-intent keywords
- Include long-tail keywords
- Include viral Shorts-related keywords when relevant
- Do not generate irrelevant tags

ADDITIONAL RULES:
- Analyze the video's strongest viral angle before generating metadata
- Prioritize CTR first, then retention, then SEO
- Avoid generic titles
- Avoid repetitive keywords
- Avoid hashtags in the title
- Description may include up to 3 relevant hashtags if appropriate
- Output must be in English

Return ONLY valid JSON.

{
    "title": "",
    "description": "",
    "tags": []
}
"""


def extract_json(text):

    text = text.strip()

    text = re.sub(
        r"^```json",
        "",
        text
    )

    text = re.sub(
        r"```$",
        "",
        text
    )

    return json.loads(text)


def generate_youtube_metadata(
    analysis
):

    response = model.generate_content([
        PROMPT,
        json.dumps(
            analysis,
            indent=2
        )
    ])

    return extract_json(
        response.text
    )
