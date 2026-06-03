import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F

# Path to fine-tuned DistilRoBERTa model
MODEL_PATH = "models/model/distilroberta_finetuned"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

# Use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

print(" Text model (DistilRoBERTa) loaded successfully")


def preprocess_text(text):
    """Clean and tokenize input text."""
    text = str(text).lower().strip()
    encoding = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=256
    )
    return encoding


def predict_text(text: str):
    """Run fake news detection on text input."""
    inputs = preprocess_text(text)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1).cpu().numpy().flatten()

    fake_prob, real_prob = probs[0], probs[1]
    label = "Fake" if fake_prob >= real_prob else "Real"
    confidence = fake_prob if label == "Fake" else real_prob

    return label, round(float(confidence), 4)
