from flask import Flask, request, jsonify, render_template
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")  # ✅ THIS FIXES THE 404
def home():
    return render_template("index.html")

@app.route("/api/country")
def country():
    name = request.args.get("name", "").strip()

    if not name:
        return jsonify({"error": "Country required"}), 400

    url = f"https://restcountries.com/v3.1/name/{name}?fullText=true"
    r = requests.get(url)

    if r.status_code != 200:
        return jsonify({"error": "Country not found"}), 404

    data = r.json()[0]

    # 🔧 edited code (safe currency handling)
    currency_list = list(data.get("currencies", {}).values())
    currency_data = currency_list[0] if currency_list else {"name": "N/A", "symbol": ""}

    return jsonify({
        "country": data["name"]["common"],
        "capital": data.get("capital", ["N/A"])[0],
        "population": data["population"],
        "region": data["region"],
        "language": ", ".join(data.get("languages", {}).values()),
        "currency_name": currency_data["name"],
        "currency_symbol": currency_data.get("symbol", ""),
        "flag": data["flags"]["png"]
    })

if __name__ == "__main__":
    app.run(debug=True)
