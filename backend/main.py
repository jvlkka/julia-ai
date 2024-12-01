from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import openai
import os
from dotenv import load_dotenv
import time
import json
import hashlib
from datetime import datetime, timedelta

load_dotenv()

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:5173",
    "https://julia-ai.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

# Cache configuration
CACHE_DURATION = 3600  # Cache duration in seconds (1 hour)
response_cache: Dict[str, dict] = {}

def get_cache_key(endpoint: str, params: dict) -> str:
    """Generate a cache key from endpoint and parameters"""
    param_str = json.dumps(params, sort_keys=True)
    return hashlib.md5(f"{endpoint}:{param_str}".encode()).hexdigest()

def get_cached_response(cache_key: str) -> Optional[dict]:
    """Get response from cache if it exists and is not expired"""
    if cache_key in response_cache:
        cached_item = response_cache[cache_key]
        if time.time() - cached_item['timestamp'] < CACHE_DURATION:
            return cached_item['data']
        else:
            del response_cache[cache_key]
    return None

def cache_response(cache_key: str, response_data: dict):
    """Cache the response with timestamp"""
    response_cache[cache_key] = {
        'data': response_data,
        'timestamp': time.time()
    }

class IdeaRequest(BaseModel):
    topic: str
    tone: str
    language: str

class TitleRequest(BaseModel):
    idea: str
    tone: str
    language: str

class ThumbnailRequest(BaseModel):
    title: str
    tone: str
    language: str

class HookRequest(BaseModel):
    title: str
    tone: str
    language: str

async def generate_openai_response(messages: list, cache_key: str) -> dict:
    """Generate response from OpenAI with caching"""
    try:
        # Check cache first
        cached_response = get_cached_response(cache_key)
        if cached_response:
            return cached_response

        # Generate new response
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=messages,
            temperature=0.7
        )
        
        result = {
            'status': 'success',
            'content': response.choices[0].message.content
        }
        
        # Cache the response
        cache_response(cache_key, result)
        return result
        
    except openai.RateLimitError:
        raise HTTPException(
            status_code=429,
            detail="OpenAI API rate limit reached. Please wait a minute before trying again."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"status": "error", "message": str(e)}
        )

@app.post("/api/generate/ideas")
async def generate_ideas(request: IdeaRequest):
    cache_key = get_cache_key("ideas", request.dict())
    
    prompt = f"""Generate 5 engaging YouTube video ideas about {request.topic}. 
    The ideas should be in {request.language} and use a {request.tone} tone.
    Each idea should be unique and have potential for high engagement.
    Format the response as a numbered list (1., 2., etc.)."""

    messages = [
        {"role": "system", "content": "You are a creative YouTube content strategist."},
        {"role": "user", "content": prompt}
    ]

    response = await generate_openai_response(messages, cache_key)
    ideas = [idea.strip() for idea in response['content'].split("\n") if idea.strip()]
    return {"status": "success", "ideas": ideas}

@app.post("/api/generate/title")
async def generate_title(request: TitleRequest):
    cache_key = get_cache_key("title", request.dict())
    
    prompt = f"""Create 5 catchy YouTube titles for a video about: {request.idea}
    The title should be in {request.language} and use a {request.tone} tone.
    Make it engaging and optimized for YouTube search.
    Format the response as a numbered list (1., 2., etc.)."""

    messages = [
        {"role": "system", "content": "You are a YouTube title optimization expert."},
        {"role": "user", "content": prompt}
    ]

    response = await generate_openai_response(messages, cache_key)
    titles = [title.strip() for title in response['content'].split("\n") if title.strip()]
    return {"status": "success", "titles": titles}

@app.post("/api/generate/thumbnail")
async def generate_thumbnail_text(request: ThumbnailRequest):
    cache_key = get_cache_key("thumbnail", request.dict())
    
    prompt = f"""Create 3 attention-grabbing text options for a YouTube thumbnail.
    The video title is: {request.title}
    Language: {request.language}
    Tone: {request.tone}
    Make it short, impactful, and easy to read on a thumbnail.
    Format the response as a numbered list (1., 2., etc.)."""

    messages = [
        {"role": "system", "content": "You are a YouTube thumbnail design expert."},
        {"role": "user", "content": prompt}
    ]

    response = await generate_openai_response(messages, cache_key)
    thumbnail_texts = [text.strip() for text in response['content'].split("\n") if text.strip()]
    return {"status": "success", "thumbnail_texts": thumbnail_texts}

@app.post("/api/generate/hook")
async def generate_hook(request: HookRequest):
    cache_key = get_cache_key("hook", request.dict())
    
    prompt = f"""Create 3 compelling video hooks/intros for a YouTube video titled: {request.title}
    Language: {request.language}
    Tone: {request.tone}
    Each hook should be 2-3 sentences that grab attention in the first 5 seconds.
    Format the response as a numbered list (1., 2., etc.)."""

    messages = [
        {"role": "system", "content": "You are a YouTube video hook writing expert."},
        {"role": "user", "content": prompt}
    ]

    response = await generate_openai_response(messages, cache_key)
    hooks = [hook.strip() for hook in response['content'].split("\n") if hook.strip()]
    return {"status": "success", "hooks": hooks}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
