from flask import Flask, send_from_directory, request, jsonify
import requests

app = Flask(__name__, static_folder="static")

ROBLOX_API_BASE = "https://users.roblox.com/v1/"
HEADSHOT_API = "https://www.roblox.com/headshot-thumbnail/image?userId={}&width=420&height=420&format=png"

def getUID(user):
    url = f"{ROBLOX_API_BASE}users/search?keyword={username}&limit=1"
    response = requests.get(url).json()
    try:
        return response['data'][0]['id']
    except (IndexError, KeyError):
        return None

def getUP(uid):
    presURL = "https://presence.roblox.com/v1/presence/users"
    payload = {"userIds": [uid]}
    response = requests.post(presURL, json=payload).json()

    try:
        user_data = response['userPresences'][0]
        if user_data['placeId']:
            return {
                "placeId": user_data["placeId"],
                "serverId": user_data["gameId"]
            }
    except (IndexError, KeyError):
        return None

@app.route('/')
def home():
    return send_from_directory("static", "index.html")

@app.route('/search', methods=['POST'])
def search():
    username = request.json.get("username")
    uid = getUID(username)

    if not uid:
        return jsonify({"error": "User not found"}), 404

    headshot_url = HEADSHOT_API.format(UID)
    server_data = getUP(uid)

    return jsonify({
        "uid": uid,
        "headshot": headshot_url,
        "server_data": server_data
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
