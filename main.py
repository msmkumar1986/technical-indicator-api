from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import numpy as np
import math

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL for stricter access
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
        return {"error": f"Need at least {period + 1} prices to compute RSI."}

    deltas = np.diff(close)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)

    avg_gain = np.zeros(len(close))
    avg_loss = np.zeros(len(close))

    avg_gain[period] = np.mean(gains[:period])
    avg_loss[period] = np.mean(losses[:period])

    for i in range(period + 1, len(close)):
        avg_gain[i] = (avg_gain[i - 1] * (period - 1) + gains[i - 1]) / period
        avg_loss[i] = (avg_loss[i - 1] * (period - 1) + losses[i - 1]) / period

    rs = np.divide(avg_gain, avg_loss, out=np.zeros_like(avg_gain), where=avg_loss != 0)
    rsi = 100 - (100 / (1 + rs))

    rsi_values = [
        round(float(r), 2) if not math.isnan(r) and not math.isinf(r) else None
        for r in rsi
    ]

    # Return only values starting from index == period (to match RSI convention)
    return {"rsi": rsi_values[period:]}
