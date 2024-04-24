from flask import Flask, request, jsonify
import requests
import json
from checkSignature import decode_token
from upload import delete_file, upload_file
from decouple import config


app = Flask(__name__)


def handle_exception(e, status_code=500):
    return jsonify({'error': str(e)}), status_code


@app.route('/validate-document', methods=['POST'])
def verifyInsurance():
    try:
        # check signature
        token = request.headers.get('Authorization')
        profile = request.args.get('profile')
        if not token:
            return 'Missing token', 401
        decode_token(token)
        if 'front' not in request.files:
            return 'Missing file parts'

        front_file = request.files['front']
        if front_file.filename == '':
            return 'No selected file'
        back_file = request.files['back'] if 'back' in request.files else None
        face_file = request.files['face'] if 'face' in request.files else None

        # read as encoded base64
        frontUrl = upload_file(front_file)
        if not frontUrl:
            return "Failed to upload front file"
        backUrl = upload_file(back_file) if back_file else None
        faceUrl = upload_file(face_file) if face_file else None

        

        url = "https://api2.idanalyzer.com/scan"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-API-KEY": config('ID_ANLYZERE_KEY')
        }

        payload = {
            "document": frontUrl,
            "documentBack": backUrl if back_file.filename else None,
            "face": faceUrl if face_file.filename else None,
            "profile": profile or config("PROFILE")
        }
        if not back_file.filename:
            del payload["documentBack"]
        if not face_file.filename:
            del payload["face"]

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            return "Failed to process the request. Status code:", response.status_code
        delete_file(front_file.filename)
        if back_file.filename:
            delete_file(back_file.filename)
        if face_file.filename:
            delete_file(face_file.filename)
        parsed_data = json.loads(response.text)

        return jsonify(parsed_data), 200

    except Exception as e:
        return handle_exception(e.args[0], e.args[1] if len(e.args) > 1 else 500)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
