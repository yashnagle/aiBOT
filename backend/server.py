from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)

@app.route("/", methods = ['GET', 'POST'])
@cross_origin()
def query():
    if request.method == 'GET':
        print('GET request')
        return jsonify({'request_type':'GET'})
    elif request.method == 'POST':
        print('POST request')
        return jsonify({'request_type':'POST'})

    
if __name__ == '__main__':
    app.run(debug = True)