from fastapi import APIRouter, UploadFile, File
from ultralytics import YOLO
import os
import shutil

router = APIRouter(
    prefix="/vision",
    tags=["Vision"]
)

model = YOLO("yolov8n.pt")


@router.post("/detect")
def detect_objects(
    file: UploadFile = File(...)
):
    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join(
        "uploads",
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    results = model(file_path)

    detections = []

    for result in results:

        boxes = result.boxes

        for box in boxes:

            class_id = int(
                box.cls[0]
            )

            confidence = float(
                box.conf[0]
            )

            detections.append({
                "object": model.names[class_id],
                "confidence": round(
                    confidence,
                    3
                )
            })

    return {
        "message": "Object detection completed",
        "detections": detections
    }