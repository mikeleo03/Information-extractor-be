from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
from src.AppExtractor import *
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

data = {}
# Main pages
@app.route("/", methods=["POST","GET"])

# Keyword gather
@app.route('/api/keyword', methods=['GET'])
@cross_origin()
def get_keyword():
    global data
    return jsonify(data)

# Search post process
@app.route('/api/search', methods=['POST'])
@cross_origin()
def search_keywords():
    if(not request.json or not ('keyword' in request.json and 'data' in request.json)):
        abort(400)

    global data
    data = {
        'keyword': request.json['keyword'],
        'data': request.json['data'],
        'algorithm': request.json['algorithm'],
    }
    print(data)
    return jsonify({'result': data}), 201

# Information extraction process
@app.route('/api/extract_information', methods=['GET'])
@cross_origin()
def extract_information():
    global data

    extraction = {
        'keyword': data['keyword'],
        'data': [],
        'algorithm': data['algorithm'],
    }

    for file in data['data']:
        extraction['data'].append(BeginExtraction(data['keyword'], data['algorithm'], file['filename'], file['content']))

    return jsonify({"result": extraction})
    
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
