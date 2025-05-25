# 📈 RSI Calculator API

A simple RSI (Relative Strength Index) calculator API for developers — send closing prices, get back RSI values.

---

## 📦 Example Usage

### ✅ How to Use the RSI API

Send a POST request to this endpoint:

POST https://your-api-name.onrender.com/rsi

css
Copy
Edit

**Request Body:**

```json
{
  "close": [122.5, 124.1, 123.2, 125.3, 127.0, 128.2, 129.8, 131.4, 132.9, 134.5, 135.8, 136.2, 135.9, 137.0, 138.2],
  "period": 14
}
Response:

json
Copy
Edit
{
  "rsi": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, 93.37]
}
🐍 Python Example
python
Copy
Edit
import requests

url = "https://your-api-name.onrender.com/rsi"

data = {
    "close": [122.5, 124.1, 123.2, 125.3, 127.0, 128.2, 129.8, 131.4, 132.9, 134.5, 135.8, 136.2, 135.9, 137.0, 138.2],
    "period": 14
}

response = requests.post(url, json=data)
print(response.json())
🟢 Node.js Example
js
Copy
Edit
const fetch = require('node-fetch');

const url = "https://your-api-name.onrender.com/rsi";

const data = {
  close: [122.5, 124.1, 123.2, 125.3, 127.0, 128.2, 129.8, 131.4, 132.9, 134.5, 135.8, 136.2, 135.9, 137.0, 138.2],
  period: 14
};

fetch(url, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(data)
})
  .then(res => res.json())
  .then(result => {
    console.log(result);
  });
