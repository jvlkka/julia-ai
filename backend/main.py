from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import openai
import os
from dotenv import load_dotenv
import time
import uvicorn

load_dotenv()

app = FastAPI()

# Rate limiting configuration
RATE_LIMIT_DURATION = 60  # seconds
MAX_REQUESTS = 20  # requests per duration
request_history: Dict[str, list] = {}

# Configure CORS
origins = [
    "http://localhost:5173",    # Local development
    "https://julia-ai.vercel.app",  # Production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

def check_rate_limit(client_ip: str) -> bool:
    current_time = time.time()
    if client_ip not in request_history:
        request_history[client_ip] = []
    
    # Remove old requests
    request_history[client_ip] = [
        timestamp for timestamp in request_history[client_ip]
        if current_time - timestamp < RATE_LIMIT_DURATION
    ]
    
    # Check if rate limit is exceeded
    if len(request_history[client_ip]) >= MAX_REQUESTS:
        return False
    
    # Add new request
    request_history[client_ip].append(current_time)
    return True

@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    client_ip = request.client.host
    if not check_rate_limit(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later."
        )
    return await call_next(request)

# Error handler for OpenAI API errors
async def handle_openai_error(func):
    try:
        return await func()
    except openai.RateLimitError:
        raise HTTPException(
            status_code=429,
            detail="OpenAI API rate limit exceeded. Please try again later."
        )
    except openai.APIError:
        raise HTTPException(
            status_code=500,
            detail="Error with OpenAI API. Please try again later."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

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
    async def generate_ideas_async():
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

    return await handle_openai_error(generate_ideas_async)

@app.post("/api/generate/title")
async def generate_title(request: TitleRequest):
    async def generate_title_async():
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

    return await handle_openai_error(generate_title_async)

@app.post("/api/generate/thumbnail")
async def generate_thumbnail_text(request: ThumbnailRequest):
    async def generate_thumbnail_text_async():
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

    return await handle_openai_error(generate_thumbnail_text_async)

@app.post("/api/generate/hook")
async def generate_hook(request: HookRequest):
    async def generate_hook_async():
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

    return await handle_openai_error(generate_hook_async)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
