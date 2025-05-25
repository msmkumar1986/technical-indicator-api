from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import numpy as np
import math

app = FastAPI()

class RSIRequest(BaseModel):
    close: List[float]
    period: int = 14

@app.post("/rsi")
def calculate_rsi(data: RSIRequest):
    close = np.array(data.close)
    period = data.period

    if len(close) < period:
        return {"error": "Not enough data points"}

    deltas = np.diff(close)
    gain = np.where(deltas > 0, deltas, 0)
    loss = np.where(deltas < 0, -deltas, 0)

    avg_gain = np.empty_like(close)
    avg_loss = np.empty_like(close)

    avg_gain[:period] = np.nan
    avg_loss[:period] = np.nan

    avg_gain[period] = gain[:period].mean()
    avg_loss[period] = loss[:period].mean()

    for i in range(period + 1, len(close)):
        avg_gain[i] = (avg_gain[i - 1] * (period - 1) + gain[i - 1]) / period
        avg_loss[i] = (avg_loss[i - 1] * (period - 1) + loss[i - 1]) / period

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    # Fix NaNs/Infs by replacing with None
    safe_rsi = [None if (math.isnan(x) or math.isinf(x)) else round(x, 2) for x in rsi]

    return {"rsi": safe_rsi}
