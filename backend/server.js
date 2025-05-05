const express = require("express");
const axios   = require("axios");
const cors    = require("cors");

const app = express();
const PORT = 5000;

// Your subscription key from the working curl:
const SUBSCRIPTION_KEY = "93ba15f29db644db87ada34d1efc2e2e";

app.use(cors());

app.get("/tilbud", async (req, res) => {
  try {
    const response = await axios.get(
      "https://minetilbud.azure-api.net/cloudApi/web/Search",
      {
        params: {
          search: "Smirnoff Ice",
          numberOfResults: 20
        },
        headers: {
          "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
      }
    );

    // The JSON you saw has an `adverts` array:
    const raw = response.data.adverts || [];

    // Map to the shape your React app expects:
    const tilbud = raw.map(item => ({
      name:  item.title,
      price: item.price.toString() + " DKK", 
      store: item.customerName,
      image: item.imageUrl
    }));

    res.json({ tilbud });
  } catch (err) {
    console.error("Error fetching offers:", err.message);
    res.status(500).json({ error: "Failed to fetch offers", details: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
