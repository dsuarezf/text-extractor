""" Text Extractor Service

This module is a Flask application serving a RESTFul API to extract plain text from files
in Word, PDF and HTML formats.

"""
import logging
import os
import re
import urllib
from subprocess import Popen, PIPE

from flask import Flask, request
from werkzeug.utils import secure_filename


class RawTextNormalizer:
    """Class to normalize raw text: remove extra whitespaces, meta-characters and alike"""

    def __init__(self, metacharacters=True, whitespaces=True, hyphenation=True):
        """Constructor"""

        self.metacharacters = metacharacters
        self.whitespaces = whitespaces
        self.hyphenation = hyphenation

    def normalize(self, raw_text):
        """Executes the normalization over a raw text"""

        if self.whitespaces:
            raw_text = re.sub(r' +', ' ', raw_text)
            raw_text = re.sub(re.compile('^ ', re.MULTILINE), '', raw_text)
            raw_text = re.sub(re.compile(' $', re.MULTILINE), '', raw_text)

        if self.metacharacters:
            raw_text = re.sub(r'', '', raw_text)
            raw_text = re.sub(r'\xad', '-', raw_text)  # metacharacter for dashes

        if self.hyphenation:
            raw_text = re.sub( \
                r'([A-Za-zÁÉÍÓÚáéíóúÑñ])\s*-\s*?(\n+)\s*([A-Za-zÁÉÍÓÚáéíóúÑñ]+)\s*', \
                r'\1\3\2', \
                raw_text)

        return raw_text

    def normalize_bytes(self, raw_text):
        """Normalizes non-string"""
        return self.normalize(raw_text.decode("utf-8"))


ALLOWED_EXTENSIONS = {'doc', 'docx', 'pdf', 'html', 'htm'}

# Logging configuration
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Flask configuration workflow: it loads default config present in config.py and
# tries to override it by using an environment variable that points to an external config file
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.ProductionConfig')
app.config.from_envvar('TEXT-EXTRACTOR-SETTINGS', silent=True)

# Normalizer #
NORMALIZER = RawTextNormalizer(whitespaces=False, hyphenation=False)


@app.route('/v1/health', methods=['GET'])
def index():
    """Health check endpoint"""
    return "UP"


@app.route('/api/v1.0/documents/extract', methods=['POST'])
def extract_text():
    """It extracts parameters from the HTTP request and route to the appropriate method"""

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            return convert_input_to_txt(file)
        url = request.form['url']
        if url:
            return convert_input_to_txt(urllib.request.urlopen(url))
        return "File format not supported"
    return "method not supported"


def convert_input_to_txt(file):
    """Use command line Linux tools to extract raw text from the file received as input"""
    logging.info("Converting file: %s", file.filename)
    basename, ext = os.path.splitext(secure_filename(file.filename))
    logging.debug("Basename: %s", basename)
    if ext.lower() == '.pdf':
        command = 'pdftotext -layout - -'
    elif ext.lower() == '.doc':
        command = 'catdoc'
    elif ext.lower() == '.docx':
        command = 'docx2txt'
        logging.info(command)
    elif ext.lower() == '.html' or ext.lower() == '.htm':
        command = 'html2text -utf8 -style pretty'

    else:
        logging.error("File format not supported: %s", file.filename)
        return "File format not supported"

    logging.info("Executing %s", command)
    output = Popen(command.split(),
                   stdin=PIPE, stdout=PIPE,
                   stderr=PIPE).communicate(input=file.read())[0]

    return NORMALIZER.normalize(output.decode("utf-8"))


def allowed_file(filename):
    """It checks whether the file belongs to the list of allowed extensions"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run()
