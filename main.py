# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging
import requests

import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

from flask import Flask, request


app = Flask(__name__)
api_key = "AIzaSyCbAmH8Uwxsjw8iPIPGWkL1RJEuWOMnHl8"
map_url = "https://maps.googleapis.com/maps/api/staticmap?center={},{}&zoom=17&size=400x400&maptype=satellite&key={}"
client = vision.ImageAnnotatorClient()
img_name = 'img.jpg'


@app.route('/', methods=['POST'])
def hello():
    """Return a friendly HTTP greeting."""
    req_json = request.get_json()
    lat = req_json['lat']
    lng = req_json['lng']
    image_url = map_url.format(lat, lng, api_key)

    img_data = requests.get(image_url).content
    with open(img_name, 'wb') as handler:
        handler.write(img_data)

    with io.open(img_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations
    label = next((x for x in labels if x.description == "tree"), None)

    print(labels)

    if label:
        return "{}".format(label.score)
    return "-1"


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]
