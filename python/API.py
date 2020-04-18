import argparse

import algo
import cv2
import numpy as np
import requests
import response_preparation
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/", methods=['GET'])
def api_id():
    if 'image_url' not in request.args:
        return "Error: No 'image_url' field provided. Please specify."

    url = request.args['image_url']
    resp = requests.get(url, stream=True).raw
    if resp.status != 200:
        return f"Error: resp.status = {resp.status}"

    image_enc = np.asarray(bytearray(resp.read()), dtype="uint8")
    current_image = cv2.imdecode(image_enc, cv2.IMREAD_COLOR)
    if current_image is None:
        return f"Error: Image could not be decoded (is None)"

    sorted_contours = algo.get_region_image_from_image(current_image)

    shape_paths = response_preparation.convert_to_svg(sorted_contours)

    # Use the jsonify function from Flask to convert our list of Python dictionaries to the JSON format.
    return jsonify(shape_paths)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process args.')
    parser.add_argument('--debug', action='store_true')

    args = parser.parse_args()

    if args.debug is True:
        # print('http://127.0.0.1:5000/?image_url=https://i2-prod.gazettelive.co.uk/incoming/article15432228.ece/ALTERNATES/s615/0_DRR_MGA__181118MGAklmJPG.jpg')
        print('http://127.0.0.1:5000/?image_url=https://firebasestorage.googleapis.com/v0/b/green-specs.appspot.com/o/WhatsApp%20Image%202020-04-10%20at%2017.49.29.jpeg?alt=media&token=527d2725-12de-4dc0-9d2c-ef5541fda84c')

    app.run(debug=args.debug)
