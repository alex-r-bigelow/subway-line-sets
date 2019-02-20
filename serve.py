#!/usr/bin/env python3
import argparse
import json
from flask import Flask

parser = argparse.ArgumentParser(description='Lauch the subway-line-sets server')
#parser.add_argument('-d', '--db_dir', dest='dbDir', default='/tmp/traveler-integrated',
#                    help='Directory where the bundled data is stored (default: /tmp/traveler-integrated')

args = parser.parse_args()
app = Flask(__name__)

@app.route('/')
def main():
    return app.send_static_file('index.html')

@app.route('/layout')
def layout():
    result = {}
    return json.dumps(result)

@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)

if __name__ == '__main__':
    app.run()
