from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import Design, DesignCustomization
from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

router = APIRouter(prefix="/design", tags=["Design"])

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


@router.post("/parse")
def parse_design_requirements(
    message: str,
    language: str = "English"
):
    prompt = f"""
You are an AI Architecture requirement parser.

Extract house design requirements from the user's message.

User language:
{language}

User message:
{message}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "property_type": "house",
    "plot_length": "",
    "plot_width": "",
    "bedrooms": "",
    "bathrooms": "",
    "floors": "",
    "style": "",
    "parking": false,
    "balcony": false,
    "pooja_room": false,
    "facing": "",
    "vastu": false,
    "special_requirements": []
}}

Rules:
- Do not add extra fields.
- If information is missing, use empty string.
- parking, balcony, pooja_room and vastu must be true or false.
- special_requirements must be an array.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(text)
    except:
        raise HTTPException(
            status_code=500,
            detail="Gemini returned invalid JSON"
        )

    return {
        "message": "Design requirements parsed successfully",
        "requirements": result
    }


@router.post("/generate")
def generate_designs(
    property_id: int,
    property_type: str,
    plot_length: str,
    plot_width: str,
    bedrooms: str,
    bathrooms: str,
    floors: str,
    style: str,
    parking: bool = True,
    balcony: bool = True,
    pooja_room: bool = False
):
    db: Session = SessionLocal()

    designs = []

    for option in range(1, 4):

        prompt = f"""
House Design Option {option}

Create a distinct architecture design concept.

Property Type: {property_type}
Plot Size: {plot_length} x {plot_width} feet
Bedrooms: {bedrooms}
Bathrooms: {bathrooms}
Floors: {floors}
Style: {style}
Parking: {parking}
Balcony: {balcony}
Pooja Room: {pooja_room}

Design Option:
{option}

The three options must have different space-planning approaches.
"""

        image_url = f"/design-image/{property_id}/{option}"

        design = Design(
            property_id=property_id,
            option_number=option,
            prompt=prompt,
            image_url=image_url
        )

        db.add(design)
        db.flush()

        designs.append({
            "id": design.id,
            "option": option,
            "prompt": prompt,
            "image_url": image_url
        })

    db.commit()
    db.close()

    return {
        "message": "3 design options created successfully",
        "designs": designs
    }


@router.post("/confirm/{design_id}")
def confirm_design(design_id: int):

    db: Session = SessionLocal()

    design = db.query(Design).filter(
        Design.id == design_id
    ).first()

    if not design:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Design not found"
        )

    db.query(Design).filter(
        Design.property_id == design.property_id
    ).update({
        "selected": False
    })

    design.selected = True

    db.commit()

    result = {
        "message": "Design confirmed successfully",
        "design_id": design.id,
        "option": design.option_number,
        "image_url": design.image_url
    }

    db.close()

    return result


@router.post("/customize")
def customize_design(
    design_id: int,
    room: str,
    customization_request: str
):

    db: Session = SessionLocal()

    design = db.query(Design).filter(
        Design.id == design_id
    ).first()

    if not design:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Design not found"
        )

    if not design.selected:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="Please confirm the design first"
        )

    customization = DesignCustomization(
        design_id=design_id,
        room=room,
        customization_request=customization_request
    )

    db.add(customization)

    db.commit()
    db.refresh(customization)

    result = {
        "message": "Customization request saved successfully",
        "customization_id": customization.id,
        "design_id": design_id,
        "room": room,
        "customization_request": customization_request
    }

    db.close()

    return result


@router.post("/parse-customization/{customization_id}")
def parse_customization(customization_id: int):

    db: Session = SessionLocal()

    customization = db.query(
        DesignCustomization
    ).filter(
        DesignCustomization.id == customization_id
    ).first()

    if not customization:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Customization not found"
        )

    prompt = f"""
You are an AI interior design assistant.

Room:
{customization.room}

Customization request:
{customization.customization_request}

Convert this request into structured JSON.

Return ONLY valid JSON.

Use this structure:

{{
    "room": "",
    "style": "",
    "colors": [],
    "flooring": "",
    "lighting": "",
    "furniture": [],
    "materials": [],
    "special_requirements": []
}}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(text)
    except:
        db.close()
        raise HTTPException(
            status_code=500,
            detail="Gemini returned invalid JSON"
        )

    customization.parsed_result = json.dumps(
        parsed,
        ensure_ascii=False
    )

    db.commit()

    result = {
        "message": "Customization parsed successfully",
        "customization_id": customization.id,
        "parsed_result": parsed
    }

    db.close()

    return result