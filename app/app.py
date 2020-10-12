
from flask import Flask
import os
import urllib.request
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
from wordprocess import process
import uuid
import json

UPLOAD_FOLDER = "/tmp"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = set(['.txt'])
def allowed_file(filename):
	base, ext = os.path.splitext(filename)
	return ext in ALLOWED_EXTENSIONS

@app.route('/process', methods=['POST'])
def process_request():
	if 'file' not in request.files:
		resp = jsonify({'success':False, 'errorMessage' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'errorMessage' : 'No file found'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		filename = "{}.tx".format(uuid.uuid4())
		full_fpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		file.save(full_fpath)
		r = process(fileName=full_fpath, threads=4)
		os.unlink(full_fpath)
		resp = jsonify({'success' : True, 'response': r})
		resp.status_code = 200
		return resp
	else:
		resp = jsonify({'success':False, 'errorMessage' : 'General Error'})		
		resp.status_code = 400
		return resp

if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
