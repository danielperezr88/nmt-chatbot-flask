from utils import generate_url, save_pid
from model import infer

from os import path, urandom
from binascii import hexlify
import logging
import inspect

import requests as req

from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_cors import CORS


__author__ = "Daniel Pérez"
__email__ = "dperez@human-forecast.com"


app = Flask(__name__, static_folder='browser/static', template_folder='browser/templates')
CORS(app)
MY_IP = req.get(generate_url('jsonip.com')).json()['ip']
API_IP = MY_IP
PORT = 80


def run():
    flask_options = dict(port=PORT, host='0.0.0.0')
    app.secret_key = hexlify(urandom(24))#hexlify(bytes('development_', encoding='latin-1'))
    app.run(**flask_options)


@app.route('/')
def root():
    return redirect(url_for('index'))


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/non_specific', methods=['GET'])
def non_specific():
    return render_template('non_specific.html', API_IP=API_IP if API_IP != MY_IP else 'localhost')


@app.route('/api/v1/infer', methods=['POST'])
def api_v1_infer():
    """API Function"""
    j = request.get_json()
    default_txt = "Please write something"
    r = (
          (
            infer(j['text']) if len(j['text']) > 0 else default_txt
          ) if 'text' in j else default_txt
        ) if j is not None else default_txt
    print(r)
    return jsonify(dict(input='YOU: ' + j['text'], output='CHATBOT: ' + r))


@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return 'beating', 200


# HTTP Errors handlers
@app.errorhandler(404)
def url_error(e):
    result, code = """
    Wrong URL!
    <pre>{}</pre>""".format(e), 404

    logging.info(result)

    return result, code


@app.errorhandler(500)
def server_error(e):
    result, code = """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

    logging.error(result)

    return result, code


"""@app.errorhandler(Exception)
def non_handled_exception(e):
    result, code = "A non-handled exception occurred: <pre>{}</pre> See logs for full stacktrace.".format(e), 500

    logging.error(result)

    return result, code"""


if __name__ == '__main__':

    save_pid()

    dirname = path.dirname(path.realpath(__file__))
    logfilename = inspect.getfile(inspect.currentframe()) + ".log"
    logging.basicConfig(filename=logfilename, level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info("Started")

    run()
