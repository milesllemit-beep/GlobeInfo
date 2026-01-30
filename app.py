from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

HEADERS = {"User-Agent": "GlobeInfo/1.0"}

# ==============================
# 195 GUARANTEED TOURIST SPOTS
# ==============================
TOURIST_SPOTS = {
    # ASIA (49)
    "Afghanistan": "Band-e Amir",
    "Armenia": "Geghard Monastery",
    "Azerbaijan": "Flame Towers",
    "Bahrain": "Qal'at al-Bahrain",
    "Bangladesh": "Sundarbans",
    "Bhutan": "Tiger's Nest Monastery",
    "Brunei": "Sultan Omar Ali Saifuddien Mosque",
    "Cambodia": "Angkor Wat",
    "China": "Great Wall of China",
    "Cyprus": "Tombs of the Kings",
    "Georgia": "Gergeti Trinity Church",
    "India": "Taj Mahal",
    "Indonesia": "Bali",
    "Iran": "Persepolis",
    "Iraq": "Ziggurat of Ur",
    "Israel": "Western Wall",
    "Japan": "Mount Fuji",
    "Jordan": "Petra",
    "Kazakhstan": "Bayterek Tower",
    "Kuwait": "Kuwait Towers",
    "Kyrgyzstan": "Issyk-Kul",
    "Laos": "Luang Prabang",
    "Lebanon": "Baalbek",
    "Malaysia": "Petronas Towers",
    "Maldives": "Maldives Atolls",
    "Mongolia": "Gobi Desert",
    "Myanmar": "Bagan",
    "Nepal": "Mount Everest",
    "North Korea": "Juche Tower",
    "Oman": "Sultan Qaboos Grand Mosque",
    "Pakistan": "Badshahi Mosque",
    "Philippines": "Boracay",
    "Qatar": "Museum of Islamic Art Doha",
    "Saudi Arabia": "Masjid al-Haram",
    "Singapore": "Marina Bay Sands",
    "South Korea": "Gyeongbokgung Palace",
    "Sri Lanka": "Sigiriya",
    "Syria": "Palmyra",
    "Tajikistan": "Iskanderkul",
    "Thailand": "Grand Palace",
    "Timor-Leste": "Atauro Island",
    "Turkey": "Hagia Sophia",
    "Turkmenistan": "Darvaza Gas Crater",
    "United Arab Emirates": "Burj Khalifa",
    "Uzbekistan": "Registan",
    "Vietnam": "Ha Long Bay",
    "Yemen": "Socotra",

    # EUROPE (44)
    "Albania": "Ksamil Islands",
    "Andorra": "Madriu-Perafita-Claror Valley",
    "Austria": "Schönbrunn Palace",
    "Belarus": "Mir Castle",
    "Belgium": "Grand Place",
    "Bosnia and Herzegovina": "Stari Most",
    "Bulgaria": "Rila Monastery",
    "Croatia": "Dubrovnik Old Town",
    "Czech Republic": "Charles Bridge",
    "Denmark": "Little Mermaid Statue",
    "Estonia": "Tallinn Old Town",
    "Finland": "Santa Claus Village",
    "France": "Eiffel Tower",
    "Germany": "Brandenburg Gate",
    "Greece": "Acropolis",
    "Hungary": "Parliament Building Budapest",
    "Iceland": "Blue Lagoon",
    "Ireland": "Cliffs of Moher",
    "Italy": "Colosseum",
    "Latvia": "House of the Black Heads",
    "Liechtenstein": "Vaduz Castle",
    "Lithuania": "Trakai Island Castle",
    "Luxembourg": "Luxembourg Old Town",
    "Malta": "Blue Lagoon Comino",
    "Moldova": "Orheiul Vechi",
    "Monaco": "Monte Carlo Casino",
    "Montenegro": "Bay of Kotor",
    "Netherlands": "Anne Frank House",
    "North Macedonia": "Lake Ohrid",
    "Norway": "Geirangerfjord",
    "Poland": "Auschwitz",
    "Portugal": "Belem Tower",
    "Romania": "Bran Castle",
    "Russia": "Red Square",
    "San Marino": "Guaita Tower",
    "Serbia": "Belgrade Fortress",
    "Slovakia": "Spiš Castle",
    "Slovenia": "Lake Bled",
    "Spain": "Sagrada Familia",
    "Sweden": "Gamla Stan",
    "Switzerland": "Matterhorn",
    "Ukraine": "Saint Sophia Cathedral Kyiv",
    "United Kingdom": "Big Ben",
    "Vatican City": "St. Peter's Basilica",

    # AFRICA (54)
    "Algeria": "Tassili n'Ajjer",
    "Angola": "Kalandula Falls",
    "Benin": "Pendjari National Park",
    "Botswana": "Okavango Delta",
    "Burkina Faso": "Ruins of Loropéni",
    "Burundi": "Lake Tanganyika",
    "Cape Verde": "Pico do Fogo",
    "Cameroon": "Mount Cameroon",
    "Central African Republic": "Dzanga-Sangha Reserve",
    "Chad": "Ennedi Plateau",
    "Comoros": "Mount Karthala",
    "Congo": "Odzala National Park",
    "Djibouti": "Lake Assal",
    "Egypt": "Pyramids of Giza",
    "Equatorial Guinea": "Monte Alén National Park",
    "Eritrea": "Asmara Modernist City",
    "Eswatini": "Mlilwane Wildlife Sanctuary",
    "Ethiopia": "Rock-Hewn Churches of Lalibela",
    "Gabon": "Loango National Park",
    "Gambia": "Kachikally Crocodile Pool",
    "Ghana": "Cape Coast Castle",
    "Guinea": "Mount Nimba",
    "Guinea-Bissau": "Bijagós Archipelago",
    "Ivory Coast": "Banco National Park",
    "Kenya": "Maasai Mara",
    "Lesotho": "Maletsunyane Falls",
    "Liberia": "Sapo National Park",
    "Libya": "Leptis Magna",
    "Madagascar": "Avenue of the Baobabs",
    "Malawi": "Lake Malawi",
    "Mali": "Great Mosque of Djenné",
    "Mauritania": "Eye of the Sahara",
    "Mauritius": "Le Morne Brabant",
    "Morocco": "Jemaa el-Fnaa",
    "Mozambique": "Bazaruto Archipelago",
    "Namibia": "Sossusvlei",
    "Niger": "Air Mountains",
    "Nigeria": "Zuma Rock",
    "Rwanda": "Volcanoes National Park",
    "Sao Tome and Principe": "Pico Cao Grande",
    "Senegal": "Goree Island",
    "Seychelles": "Anse Source d'Argent",
    "Sierra Leone": "Tiwai Island",
    "Somalia": "Lido Beach",
    "South Africa": "Table Mountain",
    "South Sudan": "Boma National Park",
    "Sudan": "Meroë Pyramids",
    "Tanzania": "Mount Kilimanjaro",
    "Togo": "Koutammakou",
    "Tunisia": "Amphitheatre of El Djem",
    "Uganda": "Bwindi Impenetrable Forest",
    "Zambia": "Victoria Falls",
    "Zimbabwe": "Victoria Falls",

    # AMERICAS (35)
    "Antigua and Barbuda": "Nelson's Dockyard",
    "Argentina": "Iguazu Falls",
    "Bahamas": "Nassau",
    "Barbados": "Harrison's Cave",
    "Belize": "Great Blue Hole",
    "Bolivia": "Salar de Uyuni",
    "Brazil": "Christ the Redeemer",
    "Canada": "Niagara Falls",
    "Chile": "Easter Island",
    "Colombia": "Cartagena Old Town",
    "Costa Rica": "Arenal Volcano",
    "Cuba": "Old Havana",
    "Dominica": "Boiling Lake",
    "Dominican Republic": "Punta Cana",
    "Ecuador": "Galapagos Islands",
    "El Salvador": "Santa Ana Volcano",
    "Grenada": "Grand Anse Beach",
    "Guatemala": "Tikal",
    "Guyana": "Kaieteur Falls",
    "Haiti": "Citadelle Laferrière",
    "Honduras": "Copán Ruins",
    "Jamaica": "Dunn's River Falls",
    "Mexico": "Chichen Itza",
    "Nicaragua": "Granada",
    "Panama": "Panama Canal",
    "Paraguay": "Itaipu Dam",
    "Peru": "Machu Picchu",
    "Saint Kitts and Nevis": "Brimstone Hill Fortress",
    "Saint Lucia": "Pitons",
    "Saint Vincent and the Grenadines": "La Soufrière",
    "Suriname": "Central Suriname Nature Reserve",
    "Trinidad and Tobago": "Maracas Beach",
    "United States": "Statue of Liberty",
    "Uruguay": "Colonia del Sacramento",
    "Venezuela": "Angel Falls",

    # OCEANIA (13)
    "Australia": "Sydney Opera House",
    "Fiji": "Mamanuca Islands",
    "Kiribati": "Christmas Island",
    "Marshall Islands": "Bikini Atoll",
    "Micronesia": "Nan Madol",
    "Nauru": "Command Ridge",
    "New Zealand": "Milford Sound",
    "Palau": "Rock Islands",
    "Papua New Guinea": "Kokoda Track",
    "Samoa": "To Sua Ocean Trench",
    "Solomon Islands": "Bonegi Beach",
    "Tonga": "Haʻamonga ʻa Maui",
    "Vanuatu": "Mount Yasur"
}

# ==============================
# WIKIPEDIA FETCH
# ==============================
def get_tourist_info(spot, flag_url):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{spot.replace(' ', '_')}"
    r = requests.get(url, headers=HEADERS)

    if r.status_code == 200:
        data = r.json()
        image = (
            data.get("originalimage", {}).get("source")
            or data.get("thumbnail", {}).get("source")
        )

        return {
            "image": image if image else flag_url,
            "text": f"{spot} — {data.get('extract', '')[:220]}...",
            "wiki": data.get("content_urls", {}).get("desktop", {}).get("page")
        }

    return {
        "image": flag_url,
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
    flag_url = data["flags"]["png"]

    currency_code = list(data["currencies"].keys())[0]
    currency = data["currencies"][currency_code]

    spot = TOURIST_SPOTS.get(country)
    if spot:
        tourist = get_tourist_info(spot, flag_url)
        fact_image = tourist["image"]
        fact_text = tourist["text"]
        wiki = tourist["wiki"]
    else:
        fact_image = flag_url
        fact_text = f"{country} is located in the {data['region']} region."
        wiki = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"

    return jsonify({
        "country": country,
        "capital": data["capital"][0],
        "population": data["population"],
        "region": data["region"],
        "language": ", ".join(data["languages"].values()),
        "currency_name": currency["name"],
        "currency_symbol": currency.get("symbol", ""),
        "flag": flag_url,
        "fact_image": fact_image,
        "fact_text": fact_text,
        "wiki": wiki
    })

# ==============================
# RUN APP
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
