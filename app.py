from flask import Flask, request, jsonify, send_from_directory

from backend.api import generate_market_recommendation


app = Flask(
    __name__,
    static_folder="frontend",
    static_url_path=""
)


@app.route("/")
def home():
    return send_from_directory(
        "frontend",
        "index.html"
    )


@app.route("/api/recommend", methods=["POST"]) 
def recommend():

    try:
        data = request.get_json()

        crop = data.get("crop", "")
        quantity = float(data.get("quantity", 0))
        farmer_location = data.get(
            "location",
            ""
        )

        if not crop:
            return jsonify({
                "success": False,
                "message": "Please enter a crop."
            }), 400

        if quantity <= 0:
            return jsonify({
                "success": False,
                "message": "Quantity must be greater than zero."
            }), 400

        result = generate_market_recommendation(
            crop=crop,
            quantity=quantity,
            farmer_location=farmer_location
        )

        return jsonify(result)

    except Exception as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )