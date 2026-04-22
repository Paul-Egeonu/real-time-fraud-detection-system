# 🛡️ Fraud Sentinel Pro

### Real-Time Fraud Detection System with Behavioral Intelligence

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green)
![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-orange)
![Streamlit](https://img.shields.io/badge/App-Streamlit-red)
![Status](https://img.shields.io/badge/Project-Still-in-Progress)

---

## 📌 Overview

Fraud Sentinel Pro is an end-to-end machine learning system designed to detect fraudulent financial transactions in real time.

It combines:

* Predictive modeling
* Behavioral analytics
* API-based deployment
* Interactive dashboard monitoring

This project simulates a **production-grade fintech fraud detection system** used for risk scoring, anomaly detection, and automated decision-making.

---

## 🚀 Key Features

* ⚡ Real-time fraud prediction API (FastAPI)
* 🧠 Machine learning pipeline with multiple models
* 📊 Interactive dashboard (Streamlit)
* 👤 User-level behavioral tracking
* 🔄 Live transaction simulation & fraud alerts
* 🎯 Business-driven threshold optimization
* 📈 Probability calibration for reliable predictions

---

## 🔹 Project Structure

```
fraud-sentinel-pro/
│
├── app/
│   ├── api.py
│   ├── database.py
│   ├── features.py
│   └── sentinel.py
│
├── data/
│   └── fraud_features_v2.csv
│
├── best_fraud_model_v2.pkl
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🧠 Machine Learning Pipeline

### Models Implemented

* Logistic Regression
* Random Forest
* Gradient Boosting
* XGBoost

### Enhancements

* ColumnTransformer (scaling + encoding)
* CalibratedClassifierCV (probability calibration)
* Precision-Recall based threshold optimization
* Business-weighted scoring (Recall-focused)

---

## 📊 Feature Engineering

### 🔹 Transaction Features

* `amount_usd`
* `payment_channel`
* `transaction_status`
* `currency`
* `industry`

### 🔹 Behavioral Features

* `txn_count_1h`
* `txn_count_24h`
* `failed_txn_24h`
* `user_fraud_rate`
* `merchant_fraud_rate`
* `new_device_flag`
* `new_country_flag`

### 🔹 Time-Based Features

* `hour`
* `is_weekend`

### 🔹 Derived Risk Signals

* `high_amount_flag`
* `high_velocity_flag`
* `risk_score`

---

## 🧩 System Architecture

```text
Streamlit UI (Frontend)
        ↓
FastAPI (Backend API)
        ↓
ML Model (Prediction + Calibration)
        ↓
Risk Engine (Dynamic Classification)
        ↓
SQLite Database (User Tracking)
        ↓
Live Monitoring Dashboard + Alerts
```

---

## 🔥 API Endpoints

### ✅ Health Check

```http
GET /
```

Response:

```json
{
  "status": "API running 🚀"
}
```

---

### 🚀 Fraud Prediction

```http
POST /predict
```

#### Example Request

```json
{
  "user_id": "U1389",
  "amount_usd": 250,
  "country": "Nigeria",
  "currency": "NGN",
  "industry": "fintech",
  "payment_channel": "card",
  "transaction_status": "success",
  "hour": 14,
  "is_weekend": 0
}
```

---

#### Example Response

```json
{
  "fraud_probability": 0.42,
  "prediction": 1,
  "risk_level": "MEDIUM RISK"
}
```

---

## 🧠 Risk Classification Logic

| Probability Range | Risk Level  |
| ----------------- | ----------- |
| < 20%             | LOW RISK    |
| 20% – 45%         | MEDIUM RISK |
| > 45%             | HIGH RISK   |

> Note: Model threshold is optimized separately for prediction accuracy.

---

## 🖥️ Streamlit Dashboard

### Features

* 📥 Transaction input panel
* 📊 KPI metrics (velocity, risk rates)
* 📈 Real-time fraud scoring
* 🧠 Decision engine (Approve / Review / Block)
* 📡 Live transaction stream simulation
* 🚨 Fraud alert system

---

## 🧠 Decision Engine

| Risk Level  | Action                        |
| ----------- | ----------------------------- |
| LOW RISK    | ✅ Approve transaction         |
| MEDIUM RISK | ⚠️ Require OTP / verification |
| HIGH RISK   | 🚨 Block transaction          |

---

## 💾 Database (SQLite)

Stores:

* `user_id`
* transaction details
* fraud prediction result

Used for:

* Behavioral feature generation
* User risk profiling
* Simulation of real-world fraud patterns

---

## 📦 Installation

```bash
git clone https://github.com/your-username/fraud-sentinel-pro.git
cd fraud-sentinel-pro
pip install -r requirements.txt
```

---

## ▶️ Run Locally

### Start API

```bash
uvicorn app.api:app --reload
```

---

### Start Dashboard

```bash
streamlit run app/sentinel.py
```

---

## 🌐 Deployment

### Backend (API)

* Render / Railway

### Frontend (Dashboard)

* Streamlit Cloud

---

## 📦 Docker (Optional)

```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## ⚠️ Known Limitations

* SQLite resets in cloud environments
* No authentication layer yet
* Simulated transaction data (not live production data)

---

## 🔮 Future Improvements

* Kafka real-time streaming pipeline
* PostgreSQL production database
* Model monitoring & drift detection
* Fraud ring detection (graph-based)
* User risk scoring over time
* API authentication & rate limiting

---

## 🏆 Impact

This project demonstrates how machine learning can be applied in fintech to:

* Detect fraud in real time
* Reduce financial loss
* Improve transaction security
* Automate risk-based decisions
* Simulate production fraud systems

---

## 💼 Resume Highlights

* Built an end-to-end fraud detection system using ML, FastAPI, and Streamlit
* Designed behavioral fraud features including transaction velocity and user risk scoring
* Implemented real-time scoring API with dynamic risk classification
* Developed live fraud monitoring dashboard with alert system
* Applied probability calibration and threshold tuning for business optimization

---

## 👨‍💻 Author

**Paul Egeonu**
Applied Data Scientist | Fraud & Risk Analytics

---

## ⭐ If you found this useful

Give this repo a star ⭐
