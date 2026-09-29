from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Client

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.post("/")
def create_client(
    name: str,
    email: str,
    phone: str = None,
    language: str = "English",
    db: Session = Depends(get_db)
):
    client = Client(
        name=name,
        email=email,
        phone=phone,
        language=language
    )

    db.add(client)
    db.commit()
    db.refresh(client)

    return client


@router.get("/")
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()