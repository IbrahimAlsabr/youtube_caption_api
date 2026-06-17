from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()


def extract_video_id(url_or_id: str) -> str:
    if "youtube.com/watch?v=" in url_or_id:
        return url_or_id.split("v=")[1].split("&")[0]

    if "youtu.be/" in url_or_id:
        return url_or_id.split("youtu.be/")[1].split("?")[0]

    return url_or_id


@app.get("/")
def home():
    return {"status": "ok"}


@app.get("/transcript")
def get_transcript(video: str, lang: str = "en"):
    video_id = extract_video_id(video)

    try:
        fetched = YouTubeTranscriptApi().fetch(video_id, languages=[lang])

        captions = [
            {
                "text": snippet.text,
                "start": snippet.start,
                "end": snippet.start + snippet.duration,
            }
            for snippet in fetched
        ]

        return {
            "video_id": video_id,
            "language": fetched.language_code,
            "captions": captions,
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
