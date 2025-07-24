from flask import Flask, request, jsonify
from omnidimension import Client
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)   # 👈 enable CORS for all origins




client = Client(api_key=os.environ.get("OMNIDIM_API_KEY"))

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        print("Prompt received:", prompt)
        response = client.send(text=prompt)

        # DEBUG: log what's actually returned
        print("Type:", type(response))
        print("Raw response:", response)

        # Handle if Omnidim returns string directly
        if isinstance(response, str):
            return jsonify({ "reply": response })

        # Handle if it's a dict or object with .get()
        if hasattr(response, "get"):
            return jsonify({ "reply": response.get("reply", "") })

        # Fallback — just stringify whatever it returned
        return jsonify({ "reply": str(response) })

    except Exception as e:
        print("Error:", str(e))
        return jsonify({ "error": str(e) }), 500


@app.route("/")
def home():
    return "Omnidim AI backend is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
