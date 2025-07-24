from flask import Flask, request, jsonify
from omnidimension import Client
import os

app = Flask(__name__)

client = Client(api_key=os.environ.get("OMNIDIM_API_KEY"))

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        response = client.send(text=prompt)
        reply = response.get("reply", "")
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Omnidim AI backend is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
