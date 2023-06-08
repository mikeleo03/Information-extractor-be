from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
import matcher as matcher

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

data = {}

@app.route('/api/keyword', methods=['GET'])
@cross_origin()
def get_keyword():
    global data
    return jsonify(data)


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
        filedata = {}
        filedata['filename'] = file['filename']

        parsed_content = file['content'].split('\n')
        
        print(parsed_content)

        filedata['title'] = parsed_content[0]
        filedata['date'] = parsed_content[1]
        filedata['content'] = parsed_content[2]

        information = []

        for sentence in matcher.split_to_sentences(file['content']):
            # Algorirgm choosing
            if (data['algorithm'] == "Regex"):
                sentence_html, sentence_date, sentence_count = matcher.extract_sentence_information(
                    sentence, data['keyword'].lower(), matcher.regex_matching)
            elif (data['algorithm'] == "KMP"):
                sentence_html, sentence_date, sentence_count = matcher.extract_sentence_information(
                    sentence, data['keyword'].lower(), matcher.knuth_morris_pratt)
            elif (data['algorithm'] == "BM"):
                sentence_html, sentence_date, sentence_count = matcher.extract_sentence_information(
                    sentence, data['keyword'].lower(), matcher.boyer_moore)
                
            # Output expected
            if(sentence_date == ""):
                sentence_date = filedata['date']
            if(sentence_count == ""):
                sentence_count = "Unknown"
            information.append([sentence_html, sentence_date, sentence_count])

        filedata['highlightedContent'] = information

        extraction['data'].append(filedata)

    return jsonify({"result": extraction})


if __name__ == '__main__':
    app.run(debug=True)