from fastapi import APIRouter, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.database import SessionLocal
from backend.models import Product, Merchant
import os
import shutil

router = APIRouter(
    prefix="/recommendation",
    tags=["Recommendation"]
)

CATEGORY_MAP = {
    "chair": ["chair", "furniture"],
    "couch": ["sofa", "furniture"],
    "sofa": ["sofa", "furniture"],
    "table": ["table", "furniture"],
    "bed": ["bed", "furniture"],
    "lamp": ["lighting", "light"],
    "clock": ["clock", "decor"],
    "tv": ["electronics"],
    "refrigerator": ["appliance"],
    "microwave": ["appliance"],
    "sink": ["sanitary", "kitchen"],
    "toilet": ["sanitary"],
    "tile": ["tiles", "flooring"],
    "tiles": ["tiles", "flooring"],
    "floor": ["flooring"],
    "flooring": ["flooring"],
    "marble": ["marble", "flooring"],
    "light": ["lighting", "light"]
}


def get_products(db, object_name):

    object_name = object_name.lower().strip()

    categories = CATEGORY_MAP.get(
        object_name,
        [object_name]
    )

    filters = [
        Product.category.ilike(f"%{category}%")
        for category in categories
    ]

    products = db.query(Product).join(
        Merchant,
        Product.merchant_id == Merchant.id
    ).filter(
        or_(*filters)
    ).all()

    result = []

    for product in products:

        merchant = db.query(Merchant).filter(
            Merchant.id == product.merchant_id
        ).first()

        result.append({
            "product_id": product.id,
            "product_name": product.product_name,
            "category": product.category,
            "price": product.price,
            "stock": product.stock,
            "image_url": product.image_url or "",
            "merchant_id": merchant.id,
            "business_name": merchant.business_name,
            "location": merchant.location,
            "latitude": merchant.latitude,
            "longitude": merchant.longitude
        })

    return result


@router.get("/products")
def recommend_products(object_name: str):

    db: Session = SessionLocal()

    result = get_products(
        db,
        object_name
    )

    db.close()

    return {
        "object": object_name.lower().strip(),
        "count": len(result),
        "products": result
    }


@router.post("/detect-and-recommend")
def detect_and_recommend(object_name: str):

    db: Session = SessionLocal()

    result = get_products(
        db,
        object_name
    )

    db.close()

    return {
        "detected_object": object_name.lower().strip(),
        "matched_products": len(result),
        "products": result
    }


@router.post("/image")
def image_recommendation(
    file: UploadFile = File(...)
):

    upload_dir = "uploads"

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    file_path = os.path.join(
        upload_dir,
        file.filename
    )

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "message": "Image uploaded successfully",
        "filename": file.filename,
        "path": f"/uploads/{file.filename}"
    }