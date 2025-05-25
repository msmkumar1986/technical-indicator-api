const fetch = require('node-fetch');

const url = "https://<your-app-name>.onrender.com/rsi";

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
    const rsi = result.rsi;
    rsi.forEach((val, i) => {
      console.log(`Index ${i}: RSI = ${val}`);
    });
  })
  .catch(err => console.error("Error:", err));
