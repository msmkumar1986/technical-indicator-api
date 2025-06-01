from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import numpy as np
import math

app = FastAPI()

# Allow all origins (for frontend testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class RSIRequest(BaseModel):
    close: List[float]
    period: int = 14

# RSI endpoint
@app.post("/rsi")
def calculate_rsi(data: RSIRequest):
    close = np.array(data.close, dtype=np.float64)
    period = data.period

    if len(close) < period + 1:
        return {"error": "Not enough data points for the given period."}

    # Calculate deltas
    deltas = np.diff(close)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)

    avg_gain = np.zeros_like(close)
    avg_loss = np.zeros_like(close)

    # Initial average
    avg_gain[period] = np.mean(gains[:period])
    avg_loss[period] = np.mean(losses[:period])

    # Wilder's smoothing method
    for i in range(period + 1, len(close)):
        avg_gain[i] = (avg_gain[i - 1] * (period - 1) + gains[i - 1]) / period
        avg_loss[i] = (avg_loss[i - 1] * (period - 1) + losses[i - 1]) / period

    # Calculate RS and RSI
    rs = np.divide(avg_gain, avg_loss, out=np.zeros_like(avg_gain), where=avg_loss != 0)
    rsi = 100 - (100 / (1 + rs))

    # Only return RSI values starting from index = period
    rsi_values = []
    for val in rsi[period:]:
        if math.isnan(val) or math.isinf(val) or val == 0.0:
            rsi_values.append(None)
        else:
            rsi_values.append(round(float(val), 2))

    return {"rsi": rsi_values}
