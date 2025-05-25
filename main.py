from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import numpy as np

app = FastAPI()

class RSIInput(BaseModel):
    close: List[float]
    period: Optional[int] = 14

@app.post("/rsi")
def calculate_rsi(data: RSIInput):
    close = np.array(data.close, dtype=float)
    period = data.period

    if len(close) < period + 1:
        raise HTTPException(status_code=400, detail="Not enough data points for RSI calculation")

    delta = np.diff(close)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = np.zeros_like(close)
    avg_loss = np.zeros_like(close)

    avg_gain[period] = np.mean(gain[:period])
    avg_loss[period] = np.mean(loss[:period])

    for i in range(period + 1, len(close)):
        avg_gain[i] = (avg_gain[i-1] * (period - 1) + gain[i - 1]) / period
        avg_loss[i] = (avg_loss[i-1] * (period - 1) + loss[i - 1]) / period

    rs = np.divide(avg_gain, avg_loss, out=np.zeros_like(avg_gain), where=avg_loss != 0)
    rsi = 100 - (100 / (1 + rs))
    rsi[:period] = [None] * period  # Pad initial RSI with None

    return {"rsi": rsi.tolist()}
