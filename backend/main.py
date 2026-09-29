from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from backend.database import Base, engine
from backend import models

from backend.routes.client import router as client_router
from backend.routes.merchant import router as merchant_router
from backend.routes.property import router as property_router
from backend.routes.chatbot import router as chatbot_router
from backend.routes.design import router as design_router
from backend.routes.vendor import router as vendor_router
from backend.routes.negotiation import router as negotiation_router
from backend.routes.vision import router as vision_router
from backend.routes.recommendation import router as recommendation_router

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GENERATED_DESIGNS_DIR = os.path.join(BASE_DIR, "generated_designs")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

os.makedirs(GENERATED_DESIGNS_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Architecture Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount(
    "/generated_designs",
    StaticFiles(directory=GENERATED_DESIGNS_DIR),
    name="generated_designs"
)

app.mount(
    "/uploads",
    StaticFiles(directory=UPLOADS_DIR),
    name="uploads"
)

app.mount(
    "/frontend",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend"
)

app.include_router(client_router)
app.include_router(merchant_router)
app.include_router(property_router)
app.include_router(chatbot_router)
app.include_router(design_router)
app.include_router(vendor_router)
app.include_router(negotiation_router)
app.include_router(vision_router)
app.include_router(recommendation_router)

@app.get("/")
def home():
    return FileResponse(
        os.path.join(FRONTEND_DIR, "dashboard.html")
    )

@app.get("/dashboard")
def dashboard():
    return FileResponse(
        os.path.join(FRONTEND_DIR, "dashboard.html")
    )

@app.get("/recommendation")
def recommendation_page():
    return FileResponse(
        os.path.join(FRONTEND_DIR, "recommendation.html")
    )

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/design-image/{property_id}/{option}")
def design_image(property_id: int, option: int):
    file_path = os.path.join(
        GENERATED_DESIGNS_DIR,
        f"property_{property_id}_option_{option}.png"
    )

    if not os.path.isfile(file_path):
        raise HTTPException(
            status_code=404,
            detail="Image not found"
        )

    return FileResponse(
        file_path,
        media_type="image/png"
    )