from flask import Flask, request, jsonify
from routes.check import check_route
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/check", methods=["POST"])
def check_main():
    data = request.json
    black = []
    already = 0
    rn = 0
    for track in data:
        # Every Track
        response = check_route(track)
        if response == 2:
            black.append(track["id"])
        elif response == 1:
            rn += 1
        else:
            already += 1
    out = {
        "blacklisted" : black,
        "already_indexed" : already,
        "cur" : rn
    } 
    print(out)
    return jsonify(out)
    
@app.route("/api/check-individual", methods=["POST"])
def check_individual():
    data = request.json
    # Every Track
    response = check_route(data)
    if response == 2:
        return "track is blacklisted"
    elif response == 1:
        return "track indexed"
    else:
        return "track was already indexed"