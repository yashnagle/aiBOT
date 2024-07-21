import os
import glob
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import pandas as pd
import haystack_setup
from haystack_setup import ingest
from pathlib import Path

#uploading documents to vectorDB
# response = ingest('pdf')
# print(response)


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
    if request.method == 'GET':
        print('GET request')
        return jsonify({'request_type':'GET'})
    elif request.method == 'POST':
        print('POST request')
        return jsonify({'request_type':'POST'})


@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file():

    if 'file' in request.files:
        file = request.files['file']
        # print(file)
        path = "uploads"
        file.save(os.path.join(path, file.filename))
        path = path + "/"+file.filename
        # df = pd.read_csv(path)
        # print(df.head())
        return jsonify({'status':'File Received'})
    else:
        return jsonify({'status':'File Not Received'})




    
if __name__ == '__main__':
    app.run(debug = True)