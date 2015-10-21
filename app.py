#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, abort, jsonify
from flask_wtf.csrf import CsrfProtect
app = Flask(__name__)

CsrfProtect(app)
app.debug = False                    # TODO: change this to False on real server
app.secret_key = 'SuperS3cr3tK3y'   # TODO: change this to something more yours
targetDilePath = 'upload.ino'

@app.route('/target_content_exchange/', methods=['GET', 'POST'])
def target_content_exchange():
    if 'GET' == request.method:
        f = None
        outDict = {}
        try:
            f = open(targetDilePath, 'r+')
            outDict['content'] = f.read()
            f.close()
            outDict['exists'] = True
        except FileNotFoundError:
            outDict['exists'] = False
        finally:
            return jsonify(outDict)
    elif 'POST' == request.method:
        if( not request.json ):
            print( 'No JSON data at POST request!' )
            abort(500)
        else:
            # todo: customize this according to yor particular needs.
            # Flask allows you to utilize all python features like subprocessing/IPC
            # file operations, signal sending and so on. Just be careful with incoming
            # data bewaring of some malicious operations that can be caused by invalid
            # data. Also, try to minimize execution time of routine because HTTP connection
            # doesn't like to wait too much.
            f = open(targetDilePath, 'w+')
            f.write( request.json['content'] )
            f.close()
            return jsonify({'result': 'updated'})

@app.route('/', methods=['GET'])
def index_view():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
