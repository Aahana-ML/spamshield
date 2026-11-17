import joblib
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(BASE_DIR / "spam_classifier.pkl")
threshold = joblib.load(BASE_DIR / "spam_threshold.pkl")

def predict_email(email_text):

    spam_probability = model.predict_proba([email_text])[0,1]

    prediction = int(spam_probability >= threshold)

    return {
        "prediction": "Spam" if prediction == 1 else "Ham",
        "spam_probability": float(spam_probability),
        "spam_percentage": round(float(spam_probability) * 100,2),
        "threshold": float(threshold),
        "threshold_percentage": round(float(threshold) * 100, 2)
    }

