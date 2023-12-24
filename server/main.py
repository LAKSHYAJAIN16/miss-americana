from flask import Flask, request, jsonify
from routes.check import check_route

app = Flask(__name__)

@app.route("/check", methods=["POST"])
def hello_world():
    data = request.json
    for track in data:
        # Every Track
        check_route(track)
    return jsonify(data)