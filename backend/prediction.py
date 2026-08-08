# Model loading and prediction logic
import joblib
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "department_prediction_model.pkl"

model = joblib.load(MODEL_PATH)

def predict_department(patient_data: dict):
    df = pd.DataFrame([patient_data])
    prediction = model.predict(df)[0]
    return prediction
