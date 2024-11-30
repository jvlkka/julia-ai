from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configure CORS with environment-based origins
origins = [
    "http://localhost:5173",    # Local development
    "http://localhost:3000",    # Local development alternative
    "https://julia-ai.vercel.app",  # Production Vercel URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

class IdeaRequest(BaseModel):
    topic: str
    tone: str
    language: str = "English"

class TitleRequest(BaseModel):
    idea: str
    tone: str
    language: str = "English"

class ThumbnailRequest(BaseModel):
    title: str
    tone: str
    language: str = "English"

class HookRequest(BaseModel):
    title: str
    tone: str
    language: str = "English"

@app.post("/api/generate/ideas")
async def generate_ideas(request: IdeaRequest):
    try:
        prompt = f"""Generate 5 engaging YouTube video ideas about {request.topic}. 
        The ideas should be in {request.language} and use a {request.tone} tone.
        Each idea should be unique and have potential for high engagement.
        Format the response as a numbered list (1., 2., etc.)."""

        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a creative YouTube content strategist."},
                     {"role": "user", "content": prompt}],
            temperature=0.8
        )
        
        # Process the response to create a clean list
        ideas = [idea.strip() for idea in response.choices[0].message.content.split("\n") if idea.strip()]
        return {"ideas": ideas, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e), "status": "error"})

@app.post("/api/generate/title")
async def generate_title(request: TitleRequest):
    try:
        prompt = f"""Create 5 catchy YouTube titles for a video about: {request.idea}
        The title should be in {request.language} and use a {request.tone} tone.
        Make it engaging and optimized for YouTube search.
        Format the response as a numbered list (1., 2., etc.)."""

        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a YouTube title optimization expert."},
                     {"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        titles = [title.strip() for title in response.choices[0].message.content.split("\n") if title.strip()]
        return {"titles": titles, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e), "status": "error"})

@app.post("/api/generate/thumbnail")
async def generate_thumbnail_text(request: ThumbnailRequest):
    try:
        prompt = f"""Create 3 attention-grabbing text options for a YouTube thumbnail.
        The video title is: {request.title}
        Language: {request.language}
        Tone: {request.tone}
        Make it short, impactful, and easy to read on a thumbnail.
        Format the response as a numbered list (1., 2., etc.)."""

        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a YouTube thumbnail design expert."},
                     {"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        thumbnail_texts = [text.strip() for text in response.choices[0].message.content.split("\n") if text.strip()]
        return {"thumbnail_texts": thumbnail_texts, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e), "status": "error"})

@app.post("/api/generate/hook")
async def generate_hook(request: HookRequest):
    try:
        prompt = f"""Create 3 compelling video hooks/intros for a YouTube video titled: {request.title}
        Language: {request.language}
        Tone: {request.tone}
        Each hook should be 2-3 sentences that grab attention in the first 5 seconds.
        Format the response as a numbered list (1., 2., etc.)."""

        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a YouTube video hook writing expert."},
                     {"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        hooks = [hook.strip() for hook in response.choices[0].message.content.split("\n") if hook.strip()]
        return {"hooks": hooks, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e), "status": "error"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
