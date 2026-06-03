import torch
import torch.nn.functional as F
import torchvision.models as models
import torchvision.transforms as T
import cv2
import os
import numpy as np
from decord import VideoReader, cpu, gpu # type: ignore

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

MODEL_PATH = "models/model/checkpoint_epoch12.pth"
NUM_FRAMES = 16
TARGET_SIZE = (224, 224)


def load_video_model():
    """Load pretrained R3D-18 + ResNet50 models."""
    resnet_model = models.resnet50(weights=None)
    resnet_model.fc = torch.nn.Linear(resnet_model.fc.in_features, 2)

    r3d_model = models.video.r3d_18(weights=None)
    r3d_model.fc = torch.nn.Linear(r3d_model.fc.in_features, 2)

    checkpoint = torch.load(MODEL_PATH, map_location=DEVICE)
    resnet_model.load_state_dict(checkpoint["resnet"])
    r3d_model.load_state_dict(checkpoint["r3d"])

    resnet_model.to(DEVICE).eval()
    r3d_model.to(DEVICE).eval()

    print(" Video model (R3D-18 + ResNet50) loaded successfully")
    return resnet_model, r3d_model


def preprocess_video(video_path):
    """Extract and preprocess frames from video."""
    vr = VideoReader(video_path, ctx=gpu(0) if torch.cuda.is_available() else cpu())
    total_frames = len(vr)
    indices = np.linspace(0, total_frames - 1, NUM_FRAMES, dtype=int)
    frames = vr.get_batch(indices).asnumpy()

    transform = T.Compose([
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]),
    ])

    processed = []
    for frame in frames:
        frame_resized = cv2.resize(frame, TARGET_SIZE)
        processed.append(transform(frame_resized))

    clip = torch.stack(processed)
    return clip.unsqueeze(0).to(DEVICE)


def predict_video(video_path):
    """Run deepfake detection on video (swapped: 0=Real, 1=Fake)."""
    resnet_model, r3d_model = load_video_model()
    clip = preprocess_video(video_path)

    # Center frame for ResNet
    center_frame = clip[:, clip.size(1)//2, :, :, :]

    with torch.no_grad():
        resnet_out = resnet_model(center_frame)
        r3d_out = r3d_model(clip.permute(0, 2, 1, 3, 4))
        combined_out = (resnet_out + r3d_out) / 2
        probs = F.softmax(combined_out, dim=1).cpu().numpy()[0]

    #  Swapped interpretation:
    real_prob, fake_prob = float(probs[0]), float(probs[1])
    label = "Real" if real_prob >= fake_prob else "Fake"
    confidence = real_prob if label == "Real" else fake_prob

    return {"label": label, "confidence": round(confidence, 3)}



if __name__ == "__main__":
    test_video = "models/model/28__outside_talking_pan_laughing.mp4"
    if os.path.exists(test_video):
        print(predict_video(test_video))
    else:
        print("No sample video found for testing.")
