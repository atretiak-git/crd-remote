""" API for hanzi convertion """
import json
from datetime import datetime

from flask import Flask
from flask import request
from flask import jsonify

from flask_restful import Resource, Api
from flask_cors import CORS

import opencc
import pinyin_jyutping_sentence

app = Flask(__name__)
CORS(app, origins=[
                   "http://127.0.0.1:80",
                   "http://127.0.0.1:5500",
                   "http://192.168.0.170:80", # ativ
                   "http://127.0.0.1:5500",
                   "http://192.168.0.170:5500", # ativ
                   "http://192.168.0.246:5500", # XPS
                  ])

api = Api(app)

# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
# other methods include put, delete, etc.
class Hello(Resource):

    # corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource
    def get(self):

        return jsonify({'message': 'hello world'})

    # Corresponds to POST request
    def post(self):
        print("ok", request.get_json())
        data = request.get_json()
        return data

""" make a file name based on the current date/time """
def make_file_name():
# Get the current date and time
    current_datetime = datetime.now()

# Format the date and time as a string
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

# Generate a human-readable file name
    file_name = f"data_{formatted_datetime}.txt"

    return file_name

# resource to dump json data to a text file server side
class Dump(Resource):
    def post(self):
        data = request.get_json()

        fn = make_file_name()
        print(fn)
        with open(fn, 'w', encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=2)  # 'indent' is an option for pretty formatting

        return len(data)

# resource to calculate the square of a number (example)
class Square(Resource):

    def get(self, num):

        return jsonify({'square': num**2})

# Chinese characters to pinyin
class Pinyin(Resource):

    def get(self, hanzi):

        return jsonify({'hanzi': hanzi, 'result': pinyin_jyutping_sentence.pinyin(hanzi)})


# traditional Chinese characters to simplified
class Simplified(Resource):

    def get(self, traditional):
        #converter = ""
        converter = opencc.OpenCC('t2s.json')

        return jsonify({'traditional': traditional, 'result': converter.convert(traditional)})

# adding the defined resources along with their corresponding urls
api.add_resource(Hello, '/hello/')
api.add_resource(Square, '/square/<int:num>')

api.add_resource(Pinyin, '/pinyin/<hanzi>')
api.add_resource(Simplified, '/simplified/<traditional>')

api.add_resource(Dump, '/dump/')

@app.route("/")
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)
