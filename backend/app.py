from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import requests

realm_id = "master2"
client_id = "backend"
client_secret = "43ns1p7sFT9H7B5baeaRqDScoPZRRrb9"

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET", "POST"])
def validate_token():
    global token
    if request.method == 'POST':
        token = request.form.get('token')
    elif request.method == 'GET':
        token = request.args.get('token')

    if token:
        print(token)
    else:
        return make_response(jsonify({"error": "Token missing"}), 400)

    try:
        response = requests.post(
            f"http://localhost:8080/realms/{realm_id}/protocol/openid-connect/token/introspect",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "token": token
            }
        )
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return make_response(jsonify({"error": "Failed to connect to the authentication server"}), 500)

    if response.status_code == 200:
        token_info = response.json()
        user_id = token_info.get("sub")
        if user_id:
            return jsonify({"message": f"Welcome, user {user_id}!"})
        else:
            return make_response(jsonify({"error": "User ID not found in token"}), 401)
    else:
        print(f"Token introspection failed with status code {response.status_code}: {response.text}")
        return make_response(jsonify({"error": "Token validation failed"}), 401)

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)