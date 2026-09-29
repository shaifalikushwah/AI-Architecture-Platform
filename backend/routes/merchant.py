from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import Merchant, Product

router = APIRouter(
    prefix="/merchant",
    tags=["Merchant"]
)


@router.post("/create")
def create_merchant(
    business_name: str,
    owner_name: str,
    email: str,
    phone: str = "",
    location: str = "",
    latitude: float = 0,
    longitude: float = 0,
    description: str = ""
):
    db: Session = SessionLocal()

    merchant = Merchant(
        business_name=business_name,
        owner_name=owner_name,
        email=email,
        phone=phone,
        location=location,
        latitude=latitude,
        longitude=longitude,
        description=description
    )

    db.add(merchant)
    db.commit()
    db.refresh(merchant)

    result = {
        "message": "Merchant created successfully",
        "merchant_id": merchant.id
    }

    db.close()

    return result


@router.post("/product")
def create_product(
    merchant_id: int,
    product_name: str,
    category: str,
    price: float,
    stock: int,
    description: str = "",
    image_url: str = ""
):
    db: Session = SessionLocal()

    merchant = db.query(Merchant).filter(
        Merchant.id == merchant_id
    ).first()

    if not merchant:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Merchant not found"
        )

    product = Product(
        merchant_id=merchant_id,
        product_name=product_name,
        category=category,
        price=price,
        stock=stock,
        description=description,
        image_url=image_url
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    result = {
        "message": "Product added successfully",
        "product_id": product.id
    }

    db.close()

    return result


@router.get("/products/{merchant_id}")
def get_products(merchant_id: int):

    db: Session = SessionLocal()

    products = db.query(Product).filter(
        Product.merchant_id == merchant_id
    ).all()

    result = []

    for product in products:
        result.append({
            "id": product.id,
            "product_name": product.product_name,
            "category": product.category,
            "price": product.price,
            "stock": product.stock,
            "description": product.description,
            "image_url": product.image_url
        })

    db.close()

    return result