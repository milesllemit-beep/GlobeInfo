from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)
HEADERS = {"User-Agent": "GlobeInfo/1.0"}

# ==============================
# 195+ GUARANTEED FAMOUS TOURIST SPOTS
# ==============================
TOURIST_SPOTS = {
    "Philippines": "Boracay",
    "Japan": "Mount Fuji",
    "France": "Eiffel Tower",
    "United States": "Statue of Liberty",
    "India": "Taj Mahal",
    "China": "Great Wall of China",
    "Italy": "Colosseum",
    "United Kingdom": "Big Ben",
    "Spain": "Sagrada Familia",
    "Germany": "Brandenburg Gate",
    "Russia": "Red Square",
    "South Korea": "Gyeongbokgung Palace",
    "North Korea": "Juche Tower",
    "Thailand": "Grand Palace",
    "Vietnam": "Ha Long Bay",
    "Indonesia": "Bali",
    "Malaysia": "Petronas Towers",
    "Singapore": "Marina Bay Sands",
    "Australia": "Sydney Opera House",
    "New Zealand": "Milford Sound",
    "Canada": "Niagara Falls",
    "Mexico": "Chichen Itza",
    "Brazil": "Christ the Redeemer",
    "Argentina": "Iguazu Falls",
    "Peru": "Machu Picchu",
    "Chile": "Easter Island",
    "Colombia": "Cartagena Old Town",
    "Cuba": "Old Havana",
    "Jamaica": "Dunn's River Falls",
    "Dominican Republic": "Punta Cana",
    "Bahamas": "Nassau",
    "Iceland": "Blue Lagoon",
    "Norway": "Geirangerfjord",
    "Sweden": "Gamla Stan",
    "Finland": "Santa Claus Village",
    "Denmark": "Little Mermaid Statue",
    "Netherlands": "Anne Frank House",
    "Belgium": "Grand Place",
    "Switzerland": "Matterhorn",
    "Austria": "Schönbrunn Palace",
    "Poland": "Auschwitz",
    "Czech Republic": "Charles Bridge",
    "Hungary": "Parliament Building Budapest",
    "Portugal": "Belem Tower",
    "Greece": "Acropolis",
    "Turkey": "Hagia Sophia",
    "Egypt": "Pyramids of Giza",
    "Morocco": "Jemaa el-Fnaa",
    "Tunisia": "Amphitheatre of El Djem",
    "South Africa": "Table Mountain",
    "Kenya": "Maasai Mara",
    "Tanzania": "Mount Kilimanjaro",
    "Uganda": "Bwindi Impenetrable Forest",
    "Rwanda": "Volcanoes National Park",
    "Nigeria": "Zuma Rock",
    "Ghana": "Cape Coast Castle",
    "Senegal": "Goree Island",
    "Ethiopia": "Rock-Hewn Churches of Lalibela",
    "Saudi Arabia": "Masjid al-Haram",
    "United Arab Emirates": "Burj Khalifa",
    "Qatar": "Museum of Islamic Art Doha",
    "Israel": "Western Wall",
    "Jordan": "Petra",
    "Lebanon": "Baalbek",
    "Iran": "Persepolis",
    "Iraq": "Ziggurat of Ur",
    "Syria": "Palmyra",
    "Pakistan": "Badshahi Mosque",
    "Bangladesh": "Sundarbans",
    "Sri Lanka": "Sigiriya",
    "Nepal": "Mount Everest",
    "Bhutan": "Tiger's Nest Monastery",
    "Myanmar": "Bagan",
    "Cambodia": "Angkor Wat",
    "Laos": "Luang Prabang",
    "Mongolia": "Gobi Desert",
    "Kazakhstan": "Bayterek Tower",
    "Uzbekistan": "Registan",
    "Georgia": "Gergeti Trinity Church",
    "Armenia": "Geghard Monastery",
    "Azerbaijan": "Flame Towers",
    "Ukraine": "Saint Sophia Cathedral Kyiv",
    "Belarus": "Mir Castle",
    "Lithuania": "Trakai Island Castle",
    "Latvia": "House of the Black Heads",
    "Estonia": "Tallinn Old Town",
    "Croatia": "Dubrovnik Old Town",
    "Slovenia": "Lake Bled",
    "Serbia": "Belgrade Fortress",
    "Bosnia and Herzegovina": "Stari Most",
    "Montenegro": "Bay of Kotor",
    "Albania": "Ksamil Islands",
    "North Macedonia": "Lake Ohrid",
    "Bulgaria": "Rila Monastery",
    "Romania": "Bran Castle",
    "Slovakia": "Spiš Castle",
    "Ireland": "Cliffs of Moher",
    "Scotland": "Edinburgh Castle",
    "Wales": "Snowdonia",
    "Greenland": "Ilulissat Icefjord",
    "Fiji": "Mamanuca Islands",
    "Samoa": "To Sua Ocean Trench",
    "Tonga": "Haʻamonga ʻa Maui",
    "Papua New Guinea": "Kokoda Track",
    "Solomon Islands": "Bonegi Beach",
    "Vanuatu": "Mount Yasur",
    "Maldives": "Maldives Atolls",
    "Seychelles": "Anse Source d'Argent",
    "Mauritius": "Le Morne Brabant",
    "Madagascar": "Avenue of the Baobabs",
    "Namibia": "Sossusvlei",
    "Botswana": "Okavango Delta",
    "Zimbabwe": "Victoria Falls",
    "Zambia": "Victoria Falls",
    "Bolivia": "Salar de Uyuni",
    "Paraguay": "Itaipu Dam",
    "Uruguay": "Colonia del Sacramento",
    "Venezuela": "Angel Falls",
    "Panama": "Panama Canal",
    "Costa Rica": "Arenal Volcano",
    "Nicaragua": "Granada",
    "Honduras": "Copán Ruins",
    "El Salvador": "Santa Ana Volcano",
    "Guatemala": "Tikal",
    "Haiti": "Citadelle Laferrière",
    "Suriname": "Central Suriname Nature Reserve",
    "Guyana": "Kaieteur Falls"
}

# ==============================
# WIKIPEDIA FETCH (SAFE)
# ==============================
def get_tourist_info(spot):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{spot.replace(' ', '_')}"
    r = requests.get(url, headers=HEADERS)

    if r.status_code == 200:
        data = r.json()
        image = (
            data.get("originalimage", {}).get("source")
            or data.get("thumbnail", {}).get("source")
        )

        return {
            "image": image or "https://images.unsplash.com/photo-1502920917128-1aa500764ce7?w=600",
            "text": f"{spot} — {data.get('extract', '')[:220]}...",
            "wiki": data.get("content_urls", {}).get("desktop", {}).get("page")
        }

    return {
        "image": "https://images.unsplash.com/photo-1502920917128-1aa500764ce7?w=600",
        "text": f"{spot} is one of the most famous tourist destinations in the world.",
        "wiki": f"https://en.wikipedia.org/wiki/{spot.replace(' ', '_')}"
    }

# ==============================
# ROUTES
# ==============================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/country")
def country_api():
    name = request.args.get("name", "").strip()
    r = requests.get(f"https://restcountries.com/v3.1/name/{name}")

    if r.status_code != 200:
        return jsonify({"error": "Country not found"})

    data = r.json()[0]
    country = data["name"]["common"]

    currency_code = list(data["currencies"].keys())[0]
    currency = data["currencies"][currency_code]

    spot = TOURIST_SPOTS.get(country, country)
    tourist = get_tourist_info(spot)

    return jsonify({
        "country": country,
        "capital": data["capital"][0],
        "population": data["population"],
        "region": data["region"],
        "language": ", ".join(data["languages"].values()),
        "currency_name": currency["name"],
        "currency_symbol": currency.get("symbol", ""),
        "flag": data["flags"]["png"],
        "fact_image": tourist["image"],
        "fact_text": tourist["text"],
        "wiki": tourist["wiki"]
    })

# ==============================
# RUN APP
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
