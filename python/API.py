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
    return calc_areas(request)


@app.route("/debug/", methods=['GET'])
def debug_api_id():
    import json

    levels_to_color_dict = {
        "Low": "000000",
        "Medium": "888888",
        "High": "ffffff",
    }

    # print(request)
    url = request.args['image_url']
    html_str = '<!DOCTYPE html><html><style>path:hover {fill: yellow;}</style></head><body>'
    html_str += f"<img src='{url}'>"

    response_json = calc_areas(request)
    response_dict = json.loads(response_json.data.decode())
    height = response_dict["height"]
    width = response_dict["width"]
    html_str += f'<svg height="{height}" width="{width}">'
    for cnt_obj in response_dict["svg_paths"]:
        _path = cnt_obj["d"]
        _color = levels_to_color_dict[cnt_obj["type"]]
        html_str += f'<path d="{_path}" fill="#{_color}" stroke="green" stroke-width="3"/>'

    html_str += f'</svg></body></html>'
    return html_str


def calc_areas(request):
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
    shape_paths = {}
    shape_paths["svg_paths"] = response_preparation.convert_to_svg(sorted_contours)
    shape_paths["height"], shape_paths["width"] = current_image.shape[:2]

    # Use the jsonify function from Flask to convert our list of Python dictionaries to the JSON format.
    return jsonify(shape_paths)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process args.')
    parser.add_argument('--debug', action='store_true')

    args = parser.parse_args()

    if args.debug is True:
        # print('http://127.0.0.1:5000/?image_url=https://i2-prod.gazettelive.co.uk/incoming/article15432228.ece/ALTERNATES/s615/0_DRR_MGA__181118MGAklmJPG.jpg')
        print('http://127.0.0.1:5000/?image_url=https://firebasestorage.googleapis.com/v0/b/green-specs.appspot.com/o/WhatsApp%20Image%202020-04-10%20at%2017.49.29.jpeg?alt=media&token=527d2725-12de-4dc0-9d2c-ef5541fda84c')
        print('http://127.0.0.1:5000/calc?image_url=https://firebasestorage.googleapis.com/v0/b/green-specs.appspot.com/o/WhatsApp%20Image%202020-04-10%20at%2017.49.29.jpeg?alt=media&token=527d2725-12de-4dc0-9d2c-ef5541fda84c')
        print('http://127.0.0.1:5000/debug?image_url=https://i2-prod.gazettelive.co.uk/incoming/article15432228.ece/ALTERNATES/s615/0_DRR_MGA__181118MGAklmJPG.jpg')
        print('http://127.0.0.1:5000/debug?image_url=https://i.ibb.co/HCscpVH/BW.jpg')
        print('http://127.0.0.1:5000/debug?image_url=https://i.ibb.co/bQxhCQY/1.jpg')
        print('http://127.0.0.1:5000/debug?image_url=https://i.ibb.co/v4jz2bY/1.jpg')

    app.run(debug=args.debug)
