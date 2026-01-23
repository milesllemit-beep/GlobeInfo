from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

def get_wiki_fact(country):
    """Fetches a high-quality image and summary from Wikipedia for the fact card."""
    # Searching for general country summary
    wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{country.replace(' ', '_')}"
    headers = {'User-Agent': 'GlobeInfoApp/1.0'}
    
    try:
        resp = requests.get(wiki_url, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "image": data.get("originalimage", {}).get("source") or data.get("thumbnail", {}).get("source"),
                "text": data.get("extract", "No details available.")[:250] + "..."
            }
    except:
        pass
    return {
        "image": "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=600",
        "text": f"{country} is known for its incredible heritage and unique geography."
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/country")
def country_api():
    name = request.args.get("name", "").strip()
    if not name: return jsonify({"error": "Empty input"}), 400

    # API 1: RestCountries for stats
    res = requests.get(f"https://restcountries.com/v3.1/name/{name}")
    if res.status_code != 200: return jsonify({"error": "Not found"}), 404

    data = res.json()[0]
    common_name = data["name"]["common"]
    
    # Currency Handling
    curr_code = list(data.get("currencies", {}).keys())[0]
    currency = data["currencies"][curr_code]

    # API 2: Wikipedia for facts and landmark image
    fact_data = get_wiki_fact(common_name)

    return jsonify({
        "country": common_name,
        "capital": data.get("capital", ["N/A"])[0],
        "population": data.get("population", 0),
        "region": data.get("region", "N/A"),
        "language": ", ".join(data.get("languages", {}).values()),
        "currency_name": f"{currency.get('name')} ({curr_code})",
        "currency_symbol": currency.get("symbol", ""),
        "flag": data["flags"]["png"],
        "fact_image": fact_data["image"],
        "fact_text": fact_data["text"]
    })

if __name__ == "__main__":
    app.run(debug=True)