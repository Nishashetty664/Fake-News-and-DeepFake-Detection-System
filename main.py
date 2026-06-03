from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

# Import model prediction functions
from models.text_model import predict_text
from models.image_model import predict_image
from models.video_model import predict_video

# Initialize FastAPI app
app = FastAPI(title="FakeDeepDetect - Fake News & Deepfake Detection")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads folder if not exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Root endpoint
@app.get("/")
def home():
    return {"message": "FakeDeepDetect API is running successfully!"}


# TEXT endpoint
@app.post("/predict_text/")
async def text_endpoint(text: str = Form(...)):
    """
    Receives text input, runs the fake news detection model,
    and returns label + confidence.
    """
    label, confidence = predict_text(text)
    return {
        "type": "text",
        "input": text,
        "prediction": label,
        "confidence": confidence
    }


# IMAGE endpoint
@app.post("/predict_image/")
async def image_endpoint(file: UploadFile = File(...)):
    """
    Receives an image file, saves temporarily,
    runs the image deepfake detection model, and returns result.
    """
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Predict
    with open(file_path, "rb") as f:
        image_bytes = f.read()
    result = predict_image(image_bytes)

    return {
        "type": "image",
        "filename": file.filename,
        "prediction": result["label"],
        "confidence": result["confidence"]
    }


# VIDEO endpoint
@app.post("/predict_video/")
async def video_endpoint(file: UploadFile = File(...)):
    """
    Receives a video file, saves temporarily,
    runs the deepfake detection model, and returns result.
    """
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Predict
    result = predict_video(file_path)

    return {
        "type": "video",
        "filename": file.filename,
        "prediction": result["label"],
        "confidence": result["confidence"]
    }
