from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re

app = Flask(
    __name__,
    static_folder="../Project_Webapp/phisbusterv2",
    static_url_path=""
)
CORS(app)

# 🔴 Final rule-based phishing detection logic
def predict_phishing(url):
    url = url.lower()

    # 0️⃣ Malformed HTTP / HTTPS check
    if url.startswith("http:///") or url.startswith("https////"):
        return 1  # Phishing

    # 1️⃣ HTTP (not secure)
    if url.startswith("http://"):
        return 1  # Phishing

    # 2️⃣ @ symbol
    if "@" in url:
        return 1  # Phishing

    # 3️⃣ IP address
    if re.search(r"\d+\.\d+\.\d+\.\d+", url):
        return 1  # Phishing

    # 4️⃣ Too many slashes
    if url.count("/") > 4:
        return 1  # Phishing

    # 5️⃣ Phishing keywords
    phishing_words = [
        "login", "verify", "bank",
        "secure", "account", "update", "confirm"
    ]
    for word in phishing_words:
        if word in url:
            return 1  # Phishing

    # 6️⃣ URL length
    if len(url) > 50:
        return 1  # Phishing

    return 0  # Safe


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data.get("url") if data else None

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    result = predict_phishing(url)

    if result == 1:
        return jsonify({"result": "Phishing Website"})
    else:
        return jsonify({"result": "Safe Website"})


if __name__ == "__main__":
    app.run()
