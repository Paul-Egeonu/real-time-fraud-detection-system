from app.database import get_connection
import pandas as pd
from datetime import datetime, timedelta


def get_user_features(user_id):
    conn = get_connection()

    query = f"""
    SELECT * FROM transactions
    WHERE user_id = '{user_id}'
    ORDER BY timestamp DESC
    """

    df = pd.read_sql(query, conn)

    if df.empty:
        return {
            "txn_count_1h": 0,
            "txn_count_24h": 0,
            "user_fraud_rate": 0,
            "avg_amount": 0
        }

    now = datetime.now()

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    last_1h = df[df["timestamp"] > now - timedelta(hours=1)]
    last_24h = df[df["timestamp"] > now - timedelta(hours=24)]

    txn_count_1h = len(last_1h)
    txn_count_24h = len(last_24h)

    fraud_rate = df["is_fraud"].mean()
    avg_amount = df["amount_usd"].mean()

    return {
        "txn_count_1h": txn_count_1h,
        "txn_count_24h": txn_count_24h,
        "user_fraud_rate": fraud_rate,
        "avg_amount": avg_amount
    }