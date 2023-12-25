import os
import sys
import random
import string

from tempfile import NamedTemporaryFile

from flask import Flask
from flask import request
from flask import send_file
from flask import make_response

from extractions import do_extract_text
from extractions import do_extract_pdf_images


app = Flask(__name__)

@app.route('/extract-text-test', methods=['GET'])
def extract_text_test():      
    form_text = '<html> \
                    <body> \
                        <p>Extract text</p> \
                        <form action="/extract-text" method="POST" enctype="multipart/form-data"> \
                            <input type="file" id="uploadFile" name="upload_file"> \
                            <br/> \
                            <input type="text" id="redactionData" name="redaction_data" style="display: none;"></input> \
                            <input type="submit"> \
                            <br/> \
                        </form> \
                    </body> \
                </html>'
    return form_text

@app.route('/extract-text', methods=['POST'])
def extract_text():
    upload = request.files['upload_file']
    filename = upload.filename
    extension = filename.split('.')[-1]
    suffix = f'.{extension}'
    redaction = request.form['redaction_data']
    with NamedTemporaryFile(suffix=suffix, buffering=0) as tmp:
        upload.save(tmp.name)
        response = make_response(do_extract_text(tmp, redaction), 200)
        response.mimetype = "text/plain"
        return response

@app.route('/extract-pdf-images-test', methods=['GET'])
def extract_pdf_images_test():      
    form_text = '<html> \
                    <body> \
                        <p>Extract PDF images</p> \
                        <form action="/extract-pdf-images" method="POST" enctype="multipart/form-data"> \
                            <input type="file" id="uploadFile" name="upload_file"> \
                            <br/> \
                            <input type="submit"> \
                        </form> \
                    </body> \
                </html>'
    return form_text

@app.route('/extract-pdf-images', methods=['POST'])
def extract_pdf_images():
    upload = request.files['upload_file']
    filename = upload.filename
    extension = filename.split('.')[-1]
    suffix = f'.{extension}'
    with NamedTemporaryFile(suffix=suffix, buffering=0) as tmp:
        upload.save(tmp.name)
        response = make_response(do_extract_pdf_images(tmp), 200)
        response.mimetype = "application/json"
        return response                  
    

@app.route('/download-pdf-images', methods=['GET'])
def download_pdf_image():
    file_location = request.args.get('file_location').replace("$", "/").split('.')[-2]
    file_name = request.args.get('file_location').split('$')[-1]
    return send_file(file_location, mimetype='application/octet-stream', download_name=file_name)

@app.route('/init', methods=['GET'])
def init():
    return '', 200

@app.route('/health', methods=['GET'])
def health():
    return '', 200

@app.route('/shutdown', methods=['GET'])
def shutdown():
    return '', 200

if __name__ == '__main__':
    if 'serve' in sys.argv:
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 80)), debug=True)
