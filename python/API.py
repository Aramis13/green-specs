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

    height, width = current_image.shape[:2]
    svg_paths = response_preparation.convert_to_svg(sorted_contours)

    ret_str = f'<svg height="{height}" width="{width}">'
    ret_str += '\n'.join(svg_paths)
    ret_str += '</svg>'
    ret_str += f'<img src="{url}">'
    return ret_str

    # Use the jsonify function from Flask to convert our list of Python dictionaries to the JSON format.
    # return jsonify(sorted_contours)


if __name__ == '__main__':
    print('http://127.0.0.1:5000/?image_url=https://i2-prod.gazettelive.co.uk/incoming/article15432228.ece/ALTERNATES/s615/0_DRR_MGA__181118MGAklmJPG.jpg')
    app.run(debug=True)
