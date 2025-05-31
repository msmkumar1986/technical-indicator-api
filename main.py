from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
import math

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace * with your frontend URL for stricter access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RSIRequest(BaseModel):
    close: List[float]
    period: int = 14

@app.post("/rsi")
def calculate_rsi(data: RSIRequest):
    close = np.array(data.close, dtype=np.float64)
    period = data.period

    if len(close) < period + 1:
        return {"error": "Not enough data points for the given period."}

    deltas = np.diff(close)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)

    avg_gain = np.zeros_like(close)
    avg_loss = np.zeros_like(close)

    avg_gain[period] = np.mean(gains[:period])
    avg_loss[period] = np.mean(losses[:period])

    for i in range(period + 1, len(close)):
        avg_gain[i] = (avg_gain[i - 1] * (period - 1) + gains[i - 1]) / period
        avg_loss[i] = (avg_loss[i - 1] * (period - 1) + losses[i - 1]) / period

    rs = np.divide(avg_gain, avg_loss, out=np.zeros_like(avg_gain), where=avg_loss!=0)
    rsi = 100 - (100 / (1 + rs))

    # Convert to list and replace out-of-range values with None
    rsi_safe = []
    for val in rsi:
        if math.isnan(val) or math.isinf(val) or val == 0.0:
            rsi_safe.append(None)
        else:
            rsi_safe.append(round(float(val), 2))

    return {"rsi": rsi_safe}
