import requests

url = "https://rsi-api.onrender.com/rsi"  # Replace with your actual Render URL

data = {
    "close": [122.5, 124.1, 123.2, 125.3, 127.0, 128.2, 129.8, 131.4, 132.9, 134.5, 135.8, 136.2, 135.9, 137.0, 138.2],
    "period": 14
}

response = requests.post(url, json=data)

if response.status_code == 200:
    result = response.json()
    rsi_values = result.get("rsi", [])
    for i, val in enumerate(rsi_values):
        print(f"Index {i}: RSI = {val}")
else:
    print("Error:", response.status_code, response.text)

