from typing import List

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from api import Api
import os

load_dotenv()

app = Flask(__name__)
api = Api(username=os.getenv('FVWB_USERNAME'), password=os.getenv('FVWB_PASSWORD'))


def require_secret(view_func):
    def decorated(*args, **kwargs):
        secret_param = request.args.get('secret')
        secret_env = os.getenv('API_SECRET')

        if secret_param != secret_env:
            return jsonify({"error": "Unauthorized"}), 401

        return view_func(*args, **kwargs)

    return decorated


@app.route('/members', methods=['GET'])
@require_secret
def get_members():
    members: List[dict] = api.get_affiliates()

    return jsonify({
        "status": "ok",
        "data": members
    })


@app.route('/calendar', methods=['GET'])
def get_calendar():
    team = request.args.get('team')
    calendar = api.get_calendar(team)

    return jsonify({
        "status": "ok",
        "data": calendar
    })


if __name__ == '__main__':
    app.run(debug=False)
