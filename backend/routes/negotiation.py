from fastapi import APIRouter, HTTPException, WebSocket
from backend.database import SessionLocal
from backend.models import Product, Negotiation

router = APIRouter(
    prefix="/negotiation",
    tags=["Negotiation"]
)


@router.post("/offer")
def make_offer(
    product_id: int,
    client_id: int,
    offered_price: float
):

    db = SessionLocal()

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:

        db.close()

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    negotiation = Negotiation(
        product_id=product.id,
        client_id=client_id,
        merchant_id=product.merchant_id,
        offered_price=offered_price,
        status="active"
    )

    db.add(negotiation)

    db.commit()

    db.refresh(negotiation)

    result = {
        "message": "Offer sent successfully",
        "negotiation_id": negotiation.id,
        "product_id": product.id,
        "product_price": product.price,
        "offered_price": offered_price,
        "status": negotiation.status
    }

    db.close()

    return result


@router.get("/{negotiation_id}")
def get_negotiation(
    negotiation_id: int
):

    db = SessionLocal()

    negotiation = db.query(
        Negotiation
    ).filter(
        Negotiation.id == negotiation_id
    ).first()

    if not negotiation:

        db.close()

        raise HTTPException(
            status_code=404,
            detail="Negotiation not found"
        )

    result = {
        "id": negotiation.id,
        "product_id": negotiation.product_id,
        "client_id": negotiation.client_id,
        "merchant_id": negotiation.merchant_id,
        "offered_price": negotiation.offered_price,
        "status": negotiation.status
    }

    db.close()

    return result


@router.websocket(
    "/ws/{negotiation_id}"
)
async def negotiation_websocket(
    websocket: WebSocket,
    negotiation_id: int
):

    await websocket.accept()

    while True:

        data = await websocket.receive_json()

        message = data.get(
            "message",
            ""
        )

        offered_price = data.get(
            "offered_price"
        )

        await websocket.send_json({
            "negotiation_id": negotiation_id,
            "message": message,
            "offered_price": offered_price,
            "status": "active"
        })