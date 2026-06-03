import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
import io

# Device setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Model path
MODEL_PATH = "models\model\efficientnet_b0_retrained4.pth"
NUM_CLASSES = 2

# Load EfficientNet-B0 architecture
model = models.efficientnet_b0(weights=None)
in_features = model.classifier[1].in_features
model.classifier[1] = nn.Linear(in_features, NUM_CLASSES)

# Load trained weights
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.to(device).eval()

print(" Image model (EfficientNet-B0) loaded successfully")

# Image normalization (ImageNet standard)
mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]

preprocess = transforms.Compose([
    transforms.Resize((240, 240)),
    transforms.ToTensor(),
    transforms.Normalize(mean, std)
])


def preprocess_image(image_bytes):
    """Convert image bytes to tensor."""
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    tensor = preprocess(image).unsqueeze(0)
    return tensor.to(device)


def predict_image(image_bytes):
    """Fake vs Real prediction for image input."""
    inputs = preprocess_image(image_bytes)

    with torch.no_grad():
        outputs = model(inputs)
        probs = F.softmax(outputs, dim=1).cpu().numpy().flatten()

    fake_prob, real_prob = probs[0], probs[1]
    label = "Fake" if fake_prob >= real_prob else "Real"
    confidence = fake_prob if label == "Fake" else real_prob

    return {
        "label": label,
        "confidence": round(float(confidence), 4)
    }
