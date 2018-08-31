import logging
import os
import urllib
from subprocess import Popen, PIPE

from flask import Flask, request
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'doc', 'docx', 'pdf', 'html', 'htm'}

# Logging configuration
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

# Flask configuration workflow: it loads default config present in config.py and tries to override it by using an
# environment variable that points to an external config file
app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
app.config.from_envvar('EXTRACT-TO-TEXT-SETTINGS', silent=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return "service extract-to-text running"


@app.route('/api/v1.0/documents/extract', methods=['POST'])
def extract_to_text():
    if request.method == 'POST':
        try:
            file = request.files['file']
        except:
            file = None
        try:
            url = request.form['url']
        except:
            url = None

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            return convert_input_to_txt(file)
        elif url:
            file = urllib.urlopen(url)
            filename = url.split('/')[-1]
            filename = secure_filename(filename)
            return convert_input_to_txt(file)
        else:
            return "File not supported."


def convert_input_to_txt(file):
    logging.info("Converting file: %s", file.filename)
    basename, ext = os.path.splitext(file.filename)
    if ext.lower() == '.pdf':
        command = 'pdftotext - -'
    elif ext.lower() == '.doc':
        command = 'catdoc'
    elif ext.lower() == '.docx':
        command = 'docx2txt'
        logging.info(command)
    elif ext.lower() == '.html' or ext.lower() == '.htm':
        command = 'html2text -utf8 -style pretty'

    else:
        logging.error("File format not supported: %s", file.filename)
        return "File format not supported."

    logging.info("Executing %s", command)
    output = Popen(command.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate(input=file.read())[0]
    logging.debug(output)

    return output


if __name__ == '__main__':
    app.run()
