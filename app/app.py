from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_caching import Cache
import asyncio
import pyppeteer
import os

app = Flask(__name__)
CORS(app)

# Configure cache (cache for 1 hour)
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 3600
PYPPETEER_CHROMIUM_REVISION = '1263111'
os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION
cache = Cache(app)

SCRAPE_URL = "https://minetilbud.dk/Tilbudssoegning?qw=Smirnoff%20Ice%20Original"


@app.route("/")
def home():
    return render_template("index.html")


async def fetch_tilbud():
    try:
        browser = await pyppeteer.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        page = await browser.newPage()

        # Sæt en brugeragent for at undgå bot-detektion
        await page.setUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )

        await page.goto(SCRAPE_URL, {"waitUntil": "domcontentloaded"})
        await asyncio.sleep(2)  # Vent for at sikre, at siden er indlæst

        # Simuler en scroll for at loade dynamisk indhold
        await page.evaluate("window.scrollBy(0, window.innerHeight)")
        await asyncio.sleep(3)

        # Vent på, at tilbuds-elementerne vises
        try:
            await page.waitForSelector(".o-search-result .o-search-result__product-list", timeout=20000)
        except:
            await browser.close()
            return []

        tilbud = await page.evaluate('''() => {
            const items = [];
            document.querySelectorAll(".o-search-result .o-search-result__product-list").forEach(element => {
                const name = element.querySelector(".o-search-result__product-title")?.innerText.trim();
                const store = element.querySelector(".o-search-result__product-customer-name")?.innerText.trim();
                const price = element.querySelector(".o-search-result__product-price")?.innerText.trim();
                const image = element.querySelector("img")?.src;

                if (name && price && store) {
                    items.push({ name, price, store, image });
                }
            });
            return items;
        }''')

        await browser.close()
        return tilbud
    except Exception as e:
        return {"error": str(e)}


@app.route("/tilbud", methods=["GET"])
def get_tilbud():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tilbud = loop.run_until_complete(fetch_tilbud())

    if "error" in tilbud:
        return jsonify({"error": "Fejl ved scraping", "details": tilbud["error"]}), 500

    if tilbud:
        return jsonify({"tilbud": tilbud})
    else:
        return jsonify({"message": "Der er ingen Smirnoff Ice på tilbud lige nu."})


if __name__ == "__main__":
    app.run(debug=True, port=5000)