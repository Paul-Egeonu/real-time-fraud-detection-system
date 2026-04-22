# ============================================================
# 🚀 FRAUD DETECTION API (USER TRACKING + FIXED LOGIC)
# ============================================================

from fastapi import FastAPI
import pandas as pd
import joblib

from app.database import create_table, get_connection
from app.features import get_user_features

# ============================================================
# INIT
# ============================================================
app = FastAPI(title="Fraud Detection API")

create_table()

# ============================================================
# LOAD MODEL
# ============================================================
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "..", "best_fraud_model_v2.pkl")

bundle = joblib.load(model_path)

model = bundle["model"]
threshold = bundle["threshold"]
features = bundle["features"]

categorical_cols = bundle["categorical_cols"]
numerical_cols = bundle["numerical_cols"]

# ============================================================
# ROOT
# ============================================================
@app.get("/")
def home():
    return {"status": "API running 🚀"}

# ============================================================
# 🧠 TYPE ENFORCER
# ============================================================
def enforce_types(df):

    for col in numerical_cols:
        if col not in df:
            df[col] = 0
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    for col in categorical_cols:
        if col not in df:
            df[col] = "unknown"
        df[col] = df[col].astype(str)

    return df

# ============================================================
# 🔥 SAFE MERGE (CRITICAL FIX)
# ============================================================
def merge_user_features(payload, user_features):
    for key, value in user_features.items():
        # ONLY fill if missing OR zero
        if key not in payload or payload[key] in [0, None, ""]:
            payload[key] = value
    return payload

# ============================================================
# PREDICT
# ============================================================
@app.post("/predict")
def predict(payload: dict):

    try:
        user_id = payload.get("user_id", "anonymous")

        # ----------------------------------
        # 🧠 GET USER FEATURES
        # ----------------------------------
        user_features = get_user_features(user_id)

        # 🔥 FIX: DO NOT OVERWRITE STREAMLIT VALUES
        payload = merge_user_features(payload, user_features)

        # ----------------------------------
        # BUILD DATAFRAME
        # ----------------------------------
        df = pd.DataFrame([payload])

        df = enforce_types(df)

        for col in features:
            if col not in df:
                df[col] = 0

        df = df[features]

        # ----------------------------------
        # PREDICT
        # ----------------------------------
        prob = model.predict_proba(df)[:, 1][0]

        prediction = int(prob >= threshold)

        # ----------------------------------
        # 🎯 DYNAMIC RISK
        # ----------------------------------
        if prob >= 0.45:
            risk = "HIGH RISK"
        elif prob >= 0.2:
            risk = "MEDIUM RISK"
        else:
            risk = "LOW RISK"

        # ----------------------------------
        # 💾 SAVE TRANSACTION
        # ----------------------------------
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO transactions 
            (user_id, amount_usd, country, payment_channel, is_fraud)
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            float(payload.get("amount_usd", 0)),
            str(payload.get("country", "")),
            str(payload.get("payment_channel", "")),
            int(prediction)
        ))

        conn.commit()
        conn.close()

        return {
            "fraud_probability": float(prob),
            "prediction": prediction,
            "risk_level": risk
        }

    except Exception as e:
        return {"error": str(e)}
