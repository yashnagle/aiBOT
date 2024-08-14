import os
import glob
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import pandas as pd
import haystack_setup
from pathlib import Path
#Imports a PyMilvus package:
from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)

ingesting_pipeline = haystack_setup.get_ingesting_pipeline()
query_pipeline = haystack_setup.get_query_pipeline()


upload_folder = 'backend/uploads'
allowed_extensions = {'csv', 'xlsx', 'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_folder
cors = CORS(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods = ['GET', 'POST'])
@cross_origin()
def query():
    print(query_pipeline)
    if request.method == 'GET':
        print('GET request')
        return jsonify({'request_type':'GET'})
    elif request.method == 'POST':
        print('POST request')
        query = request.get_json()['query']
        print(query)

        # results = query_pipeline.run(
        #     {
        #         "text_embedder": {"text": query},
        #         "prompt_builder": {"query": query},
        #         }
        # )
        # answer = results["generator"]["replies"][0]
        print(query_pipeline)
        
        return jsonify({'request_type':'POST', 'Response':'answer'})
    # return jsonify({'request_type':'POST', 'Response':'answer'})

    # connections.connect("default", host="localhost", port="19530")
    # collection = Collection('HaystackCollection')
    # print(collection.schema)
    # print(collection.description)
    # print(collection.name)
    # return jsonify({'request_type':'POST', 'Response':'answer'})
    

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file():

    if 'file' in request.files:
        file = request.files['file']
        path = "uploads"
        file.save(os.path.join(path, file.filename))
        # path = path + "/"+file.filename
        
        print(path)
        print(ingesting_pipeline.run({"file_type_router": {"sources": list(Path(path).glob(file.filename))}}))
        return jsonify({'status':'File Ingested'})
    else:
        return jsonify({'status':'File Not Received'})


if __name__ == '__main__':
    app.run(debug = True)