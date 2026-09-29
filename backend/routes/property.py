from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Property, PropertyImage
from fastapi import UploadFile, File
import os
import shutil
router = APIRouter(prefix="/properties", tags=["Properties"])


@router.post("/")
def create_property(
    client_id: int,
    property_type: str,
    length: str = None,
    width: str = None,
    location: str = None,
    description: str = None,
    db: Session = Depends(get_db)
):
    property_data = Property(
        client_id=client_id,
        property_type=property_type,
        length=length,
        width=width,
        location=location,
        description=description
    )

    db.add(property_data)
    db.commit()
    db.refresh(property_data)

    return property_data


@router.get("/")
def get_properties(db: Session = Depends(get_db)):
    return db.query(Property).all()


@router.post("/upload-image")
def upload_property_image(
    property_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image = PropertyImage(
        property_id=property_id,
        filename=file.filename,
        file_path=file_path
    )

    db.add(image)
    db.commit()
    db.refresh(image)

    return {
        "message": "Image uploaded successfully",
        "image_id": image.id,
        "property_id": property_id,
        "filename": image.filename,
        "path": image.file_path
    }