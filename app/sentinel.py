# ============================================================
# 🚀 FRAUD SENTINEL PRO — FULL SYSTEM (LIVE + SMART + ALERTS)
# ============================================================

import streamlit as st
import requests
import random
import pandas as pd
import time
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Fraud Sentinel Pro",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Fraud Sentinel Pro")
st.markdown("### Real-time Fraud Intelligence & Live Monitoring")
st.divider()

# ============================================================
# SESSION STATE (FOR LIVE STREAM)
# ============================================================
if "transactions" not in st.session_state:
    st.session_state.transactions = []


# ============================================================
# 🧠 DECISION ENGINE
# ============================================================

def get_decision(risk, prob):
    if risk == "HIGH RISK":
        return "❌ BLOCK TRANSACTION", "error"
    elif risk == "MEDIUM RISK":
        return "🔐 REQUIRE OTP / STEP-UP AUTH", "warning"
    else:
        return "✅ APPROVE TRANSACTION", "success"


# ============================================================
# SIDEBAR INPUTS (FULL VERSION)
# ============================================================
st.sidebar.header("🔍 Transaction Details")

if "user_id" not in st.session_state:
    st.session_state.user_id = f"U{random.randint(1000, 25000)}"

user_id = st.sidebar.text_input("User ID", st.session_state.user_id)
st.session_state.user_id = user_id

currency_rates = {
    "NGN": 1500,
    "GHS": 15,
    "KES": 130,
    "ZAR": 18,
    "EGP": 30,
    "RWF": 1200
}

currency = st.sidebar.selectbox("Currency", list(currency_rates.keys()))

amount_local = st.sidebar.number_input(
    f"Amount ({currency})",
    min_value=1.0,
    max_value=100_000_000.0,
    value=1000.0
)

amount_usd = amount_local / currency_rates[currency]
st.sidebar.markdown(f"💱 USD: **${amount_usd:.2f}**")

country_map = {
    "NGN": "Nigeria",
    "GHS": "Ghana",
    "KES": "Kenya",
    "ZAR": "South Africa",
    "EGP": "Egypt",
    "RWF": "Rwanda"
}

country = country_map[currency]

industry = st.sidebar.selectbox(
    "Industry",
    ["ecommerce", "fintech", "gaming", "betting", "crypto", "retail"]
)

channel = st.sidebar.selectbox(
    "Payment Channel",
    ["card", "bank_transfer", "ussd", "mobile_money"]
)

status = st.sidebar.selectbox(
    "Transaction Status",
    ["success", "failed", "reversed"]
)

hour = st.sidebar.slider("Transaction Hour", 0, 23, 12)

is_weekend_ui = st.sidebar.selectbox("Weekend?", ["No", "Yes"])
is_weekend = 1 if is_weekend_ui == "Yes" else 0

failed_flag = 1 if status != "success" else 0

# ============================================================
# 🧠 SMART FEATURE ENGINEERING (IMPORTANT)
# ============================================================

base_multiplier = min(max(amount_usd / 100, 1), 10)

txn_count_1h = int(random.randint(1, int(3 * base_multiplier)))
txn_count_24h = int(random.randint(5, int(20 * base_multiplier)))

failed_txn_24h = random.randint(0, 3 if status == "success" else 5)

new_device_flag = random.choice([0, 1])
new_country_flag = random.choice([0, 1])

merchant_fraud_rate = round(random.uniform(0.01, 0.3), 3)
user_fraud_rate = round(random.uniform(0.0, 0.15), 3)

high_amount_flag = 1 if amount_usd > 500 else 0
high_velocity_flag = 1 if txn_count_1h > 3 else 0

risk_score = (
    0.3 * high_amount_flag +
    0.3 * high_velocity_flag +
    0.2 * failed_flag +
    0.2 * is_weekend
)

# ============================================================
# 📊 KPI DASHBOARD (REAL METRICS)
# ============================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric("USD Amount", f"${amount_usd:,.2f}")
col2.metric("Txn Velocity (1h)", txn_count_1h)
col3.metric("User Fraud Rate", f"{user_fraud_rate:.2%}")
col4.metric("Merchant Risk", f"{merchant_fraud_rate:.2%}")

st.divider()

# ============================================================
# 📦 PAYLOAD BUILDER
# ============================================================

def build_payload():
    return {
        "user_id": user_id,
        "amount_usd": float(amount_usd),
        "country": str(country),
        "currency": str(currency),
        "industry": str(industry),
        "payment_channel": str(channel),
        "transaction_status": str(status),

        "hour": int(hour),
        "is_weekend": int(is_weekend),
        "failed_flag": int(failed_flag),

        "txn_count_1h": txn_count_1h,
        "txn_count_24h": txn_count_24h,
        "failed_txn_24h": failed_txn_24h,
        "new_device_flag": new_device_flag,
        "new_country_flag": new_country_flag,
        "merchant_fraud_rate": merchant_fraud_rate,
        "merchant_volume": random.randint(20, 200),
        "user_total_txns": random.randint(5, 100),
        "user_fraud_rate": user_fraud_rate,
        "high_amount_flag": high_amount_flag,
        "high_velocity_flag": high_velocity_flag,
        "risk_score": risk_score
    }

# ============================================================
# 🚀 SINGLE TRANSACTION ANALYSIS
# ============================================================

if st.button("🚀 Analyze Transaction", use_container_width=True):

    payload = build_payload()

    try:
        res = requests.post("http://127.0.0.1:8000/predict", json=payload)
        result = res.json()

        if "error" in result:
            st.error(result["error"])
        else:
            prob = result["fraud_probability"]
            risk = result["risk_level"]

            decision_text, decision_type = get_decision(risk, prob)

            st.divider()

            col1, col2 = st.columns([2, 1])

            col1.metric("Fraud Probability", f"{prob:.2%}")

            if risk == "HIGH RISK":
                col2.error("🚨 HIGH RISK")
            elif risk == "MEDIUM RISK":
                col2.warning("⚠️ MEDIUM RISK")
            else:
                col2.success("✅ LOW RISK")

            # =========================
            # 🧠 DECISION DISPLAY
            # =========================
            st.markdown("### 🧠 Decision Engine")

            if decision_type == "error":
                st.error(decision_text)
            elif decision_type == "warning":
                st.warning(decision_text)
            else:
                st.success(decision_text)

    except Exception as e:
        st.error(f"API Error: {e}")

# ============================================================
# 🔴 LIVE STREAM SIMULATION
# ============================================================

st.divider()
st.subheader("📡 Live Transaction Stream")

run = st.button("▶ Start Live Monitoring")

if run:
    placeholder = st.empty()

    for _ in range(25):

        payload = build_payload()

        try:
            res = requests.post("http://127.0.0.1:8000/predict", json=payload)
            result = res.json()

            if "error" in result:
                continue

            prob = result["fraud_probability"]
            risk = result["risk_level"]

            txn = {
                "time": datetime.now().strftime("%H:%M:%S"),
                "amount_usd": round(payload["amount_usd"], 2),
                "country": payload["country"],
                "industry": payload["industry"],
                "channel": payload["payment_channel"],
                "probability": round(prob, 3),
                "risk": risk
            }

            st.session_state.transactions.insert(0, txn)

        except:
            continue

        df = pd.DataFrame(st.session_state.transactions)

        def color_risk(val):
            if val == "HIGH RISK":
                return "background-color: red; color: white"
            elif val == "MEDIUM RISK":
                return "background-color: orange"
            else:
                return "background-color: green; color: white"

        with placeholder.container():

            col1, col2 = st.columns([2, 1])

            # =============================
            # LIVE TABLE
            # =============================
            with col1:
                st.dataframe(
                    df.style.applymap(color_risk, subset=["risk"]),
                    use_container_width=True,
                    height=400
                )

            # =============================
            # ALERT SYSTEM
            # =============================
            with col2:
                st.subheader("🚨 Alerts")

                high_risk = df[df["risk"] == "HIGH RISK"]

                if not high_risk.empty:
                    for _, row in high_risk.head(5).iterrows():

                        decision_text, _ = get_decision(row["risk"], row["probability"])

                        st.error(
                            f"{row['time']} | ${row['amount_usd']} | "
                            f"{row['country']} | {row['industry']}\n\n"
                            f"👉 {decision_text}"
                        )
                else:
                    st.success("No critical alerts")

        time.sleep(1)