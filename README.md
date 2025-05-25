# 📈 RSI Calculator API

A simple RSI (Relative Strength Index) calculator API for developers — send closing prices, get back RSI values.

---

## 📦 Example Usage

### ✅ How to Use the RSI API

Send a POST request to this endpoint:
POST https://rsi-api.onrender.com/rsi

**Request Body (JSON):**

```json
{
  "close": [122.5, 124.1, 123.2, 125.3, 127.0, 128.2, 129.8, 131.4, 132.9, 134.5, 135.8, 136.2, 135.9, 137.0, 138.2],
  "period": 14
}
```response
{
  "rsi": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, 93.37]
}

