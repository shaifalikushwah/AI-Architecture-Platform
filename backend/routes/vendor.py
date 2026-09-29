from fastapi import APIRouter
from backend.database import SessionLocal
from backend.models import Merchant, Product
from math import radians, sin, cos, sqrt, atan2

router = APIRouter(
    prefix="/vendor",
    tags=["Vendor"]
)


def distance_km(
    lat1,
    lon1,
    lat2,
    lon2
):

    earth_radius = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        +
        cos(radians(lat1))
        *
        cos(radians(lat2))
        *
        sin(dlon / 2) ** 2
    )

    return round(
        earth_radius
        *
        2
        *
        atan2(
            sqrt(a),
            sqrt(1 - a)
        ),
        2
    )


@router.get("/nearby")
def nearby_vendors(
    latitude: float,
    longitude: float,
    radius: float = 20,
    category: str = ""
):

    db = SessionLocal()

    merchants = db.query(Merchant).filter(
        Merchant.latitude.isnot(None),
        Merchant.longitude.isnot(None)
    ).all()

    result = []

    for merchant in merchants:

        distance = distance_km(
            latitude,
            longitude,
            merchant.latitude,
            merchant.longitude
        )

        if distance > radius:
            continue

        query = db.query(Product).filter(
            Product.merchant_id == merchant.id
        )

        if category:

            query = query.filter(
                Product.category.ilike(
                    f"%{category}%"
                )
            )

        products = query.all()

        result.append({
            "merchant_id": merchant.id,
            "business_name": merchant.business_name,
            "location": merchant.location,
            "distance_km": distance,
            "products": [
                {
                    "product_id": product.id,
                    "product_name": product.product_name,
                    "category": product.category,
                    "price": product.price,
                    "stock": product.stock,
                    "image_url": product.image_url or ""
                }
                for product in products
            ]
        })

    db.close()

    result.sort(
        key=lambda x: x["distance_km"]
    )

    return {
        "count": len(result),
        "vendors": result
    }