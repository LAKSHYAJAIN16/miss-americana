from flask import Flask, request, jsonify
from routes.check import check_route
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/check", methods=["POST"])
def hello_world():
    data = request.json
    print(data)
    for track in data:
        # Every Track
        check_route(track)
    return jsonify(data)