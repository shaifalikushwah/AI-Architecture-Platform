from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import errors
from dotenv import load_dotenv
import os
import time

load_dotenv()

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODELS = [
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite"
]


class ChatRequest(BaseModel):
    message: str
    language: str = "English"


@router.post("/chat")
def chat(request: ChatRequest):

    prompt = f"""
You are an AI Architecture and Interior Design assistant.

User language: {request.language}

Always answer in the same language as the user.

You can help with:
- House architecture
- Interior design
- Floor plans
- Room layouts
- Furniture
- Materials
- Colors
- Lighting
- Flooring
- Construction ideas
- Space planning
- Modern house design
- Budget-friendly design

User message:
{request.message}
"""

    last_error = None

    for model in MODELS:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                return {
                    "message": request.message,
                    "language": request.language,
                    "model": model,
                    "response": response.text
                }

            except errors.ServerError as e:
                last_error = e
                time.sleep(2 * (attempt + 1))

    raise HTTPException(
        status_code=503,
        detail="Gemini service is temporarily unavailable. Please try again."
    )