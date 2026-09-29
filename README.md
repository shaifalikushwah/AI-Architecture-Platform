# AI Architecture Platform

An AI-powered architecture and interior design platform that helps customers plan homes, generate design concepts, visualize floor plans, detect objects from uploaded images, and discover relevant products and vendors.

## Overview

This project combines:

- AI-assisted house design and planning
- Architecture chatbot assistance
- 2D and 3D visualization
- Object detection using YOLOv8
- Product recommendation and merchant discovery
- Local vendor and negotiation workflows

The application is built with FastAPI on the backend and a static HTML/CSS/JavaScript frontend.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL-compatible database setup
- Uvicorn
- YOLOv8 (Ultralytics)
- OpenCV, NumPy, Pillow
- Google Generative AI / Groq integrations
- HTML, CSS, JavaScript

## Project Structure

```text
AI_Architecture_Platform/
├── backend/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── routes/
│       ├── chatbot.py
│       ├── client.py
│       ├── design.py
│       ├── merchant.py
│       ├── negotiation.py
│       ├── property.py
│       ├── recommendation.py
│       ├── vendor.py
│       └── vision.py
├── frontend/
│   ├── 3d.html
│   ├── chatbot.html
│   ├── dashboard.html
│   ├── floorplan.html
│   ├── index.html
│   ├── merchant.html
│   ├── nearby-vendors.html
│   ├── negotiation.html
│   ├── property.html
│   ├── recommendation.html
│   ├── vision.html
│   ├── css/
│   └── js/
├── generated_designs/
├── uploads/
├── requirements.txt
├── yolov8n.pt
└── README.md
```

## Features

### Property and Design Workflow
- Capture house requirements and property details
- Generate AI-based design options
- View 2D/3D representations of designs
- Save generated design images in the project output folder

### AI Assistant
- Architecture and interior guidance through a chatbot interface
- Supports design-related queries and recommendations

### Vision and Product Matching
- Upload images for object detection
- Identify objects using YOLOv8
- Link detected objects to product recommendations

### Marketplace and Vendor Features
- Product and merchant management
- Nearby vendor discovery based on location
- Negotiation flow between customer and merchant

## Installation

1. Clone the repository.
2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

Start the backend server:

```bash
uvicorn backend.main:app --reload
```

Then open the app in the browser:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/dashboard

The frontend is served from the FastAPI app under the `/frontend` route.

## Environment Notes

Some features may require external services or API keys, including:

- Google Generative AI
- Groq
- database connection configuration

Make sure your environment variables are configured before running those modules.

## Notes

- The YOLO model file `yolov8n.pt` is expected in the project root.
- Generated images are stored under `generated_designs/`.
- Uploaded images are stored under `uploads/`.

## License

This project is provided as-is for educational and demonstration purposes.
