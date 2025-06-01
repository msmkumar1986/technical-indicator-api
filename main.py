from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import numpy as np
import math

app = FastAPI()

# CORS: Allow requests from any origin (you can restrict this to your frontend URL)
app.add_middleware(
    CORSMiddleware,
        allow_origins=["https://rsi-api-demo.onrender.com"],  # Replace "*" with ["https://your-frontend-url.com"] for stricter access
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

    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])

    rsi_values = []

    for i in range(period, len(close)):
        gain = gains[i - 1]
        loss = losses[i - 1]

        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period

        if avg_loss == 0:
            rsi = 100.0
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

        rsi_values.append(round(rsi, 2))

    return {"rsi": rsi_values}
