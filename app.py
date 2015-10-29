#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, abort, jsonify
from flask_wtf.csrf import CsrfProtect

#RadioField
from flask.ext.wtf import Form
from wtforms import RadioField
from wtforms.validators import DataRequired

#Unicode files
import codecs

from subprocess import Popen

examples = [('lcd',u'Светодиодный дисплей'),
            ('weather',u'Погодная станция'),
            ('ssd',u'7-ми сегментный индикатор'),
            ('stopwatch',u'Секундомер'),
            ('rgbled',u'Трехцветный диод')]

exampleValues = [choice[0] for choice in examples]   
        

class ExampleSelectForm(Form):
    exampleSelect = RadioField('exampleSelect',
        choices=examples,
        default='lcd',
        validators=[DataRequired()])

app = Flask(__name__)

CsrfProtect(app)
app.debug = False                    # TODO: change this to False on real server
app.secret_key = 'SuperS3cr3tK3y'   # TODO: change this to something more yours
targetFilePath = 'upload.ino'

@app.route('/target_content_exchange', methods=['GET','POST'])
def target_content_exchange():
    #exampleSelect = ExampleSelectForm()
    #import pdb; pdb.set_trace()
    if 'GET' == request.method:
        radio = request.args.get('radio')
        if radio != None: 
            f = None
            outDict = {}
            radio = request.args.get('radio')
            if radio in exampleValues:
                print(radio+' was found')
                exampleFilePath = radio+'.ino'
            else:
                print('radio value was not found')
                exampleFilePath = 'lcd.ino'
            
            try:
                f = codecs.open('examples/'+exampleFilePath, 'r+','utf-8')
                outDict['content'] = f.read()
                f.close()
                outDict['exists'] = True
            except FileNotFoundError:
                outDict['exists'] = False
            finally:
                return jsonify(outDict)
        script = request.args.get('script')        
        if script != None:
            outDict = {}
            proc = Popen(['/home/pi/test/b_test.sh'], shell=True, stderr=None, stdout=None, stdin=None, close_fds=True)
            outDict['script'] = True
            return jsonify(outDict)

        outDict = {}
        outDict['error'] = True    

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
            
            # Write data in Unicode
            f = codecs.open(targetFilePath, 'w+','utf-8')
            f.write( request.json['content'] )
            f.close()
            return jsonify({'result': 'updated'})

@app.route('/', methods=['GET'])
def index_view():
    exampleSelect = ExampleSelectForm()
    return render_template('index.html',
                            exampleSelect=exampleSelect)

if __name__ == '__main__':
    #app.run(host="0.0.0.0",port=5002,debug=True)
    app.run(host="0.0.0.0",port=8080)
