#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, abort, jsonify, url_for
from flask_wtf.csrf import CsrfProtect

#RadioField
from flask.ext.wtf import Form
from wtforms import RadioField, SelectField
from wtforms.validators import DataRequired

#Unicode files
import codecs

from subprocess import Popen
import subprocess

from celery import Celery

app = Flask(__name__)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task(bind=True)
def compile_task(self):
    self.update_state(state='PROGRESS',
                          meta={'current': 0, 'total': 1,
                                'status': 'message'})
    process = subprocess.Popen(['/home/pi/test/only_build.sh'],
                                shell=True,
                                stderr=subprocess.STDOUT,
                                stdout=subprocess.PIPE,
                                stdin=None,
                                close_fds=True)
    output = process.communicate()[0] 

    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42, 'output': output}

@celery.task(bind=True)
def upload_task(self):
    self.update_state(state='PROGRESS',
                          meta={'current': 0, 'total': 1,
                                'status': 'message'})
    process = subprocess.Popen(['/home/pi/test/only_upload.sh'],
                                shell=True,
                                stderr=subprocess.STDOUT,
                                stdout=subprocess.PIPE,
                                stdin=None,
                                close_fds=True)
    output = process.communicate()[0] 

    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42, 'output': output}


examples = [('lcd',u'Светодиодный дисплей'),
            ('weather',u'Погодная станция'),
            ('ssd',u'7-ми сегментный индикатор'),
            ('stopwatch',u'Секундомер'),
            ('rgbled',u'Трехцветный диод')]

exampleValues = [choice[0] for choice in examples]    
        
examples2 = [('nonsel', u'Выбрать пример')] + examples 
        

class ExampleSelectForm(Form):
    exampleSelect = RadioField('exampleSelect',
        choices=examples,
        default='lcd',
        validators=[DataRequired()])
    exSel2 = SelectField('exampleSelect2', choices=examples2)


CsrfProtect(app)
app.debug = False                    # TODO: change this to False on real server
app.secret_key = 'SuperS3cr3tK3y'   # TODO: change this to something more yours
targetFilePath = 'upload.ino'

@app.route('/target_content_exchange', methods=['GET','POST'])
def target_content_exchange():
    #exampleSelect = ExampleSelectForm()
    #import pdb; pdb.set_trace()
    if 'GET' == request.method:
        button = request.args.get('button')
        outDict = {}
        
        if button == None:
            outDict['result']=False
            return jsonify(outDict)

        if button == 'retrieve':
            example = request.args.get('example','lcd')
            if example in exampleValues:
                print(example+' was found')
                exampleFilePath = example+'.ino'
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
                
        # if button == 'check':
        #     #proc = Popen(['/home/pi/test/b_test.sh'], shell=True, stderr=None, stdout=None, stdin=None, close_fds=True)
        #     outDict['result'] = True
        #     task = long_task.apply_async()
        #     #url_for('taskstatus', task_id=task.id)
        #     return jsonify(outDict), 202, {'Location': url_for('taskstatus', task_id=task.id)}
        #     #return jsonify(outDict)          

        if button == 'load':
            task = upload_task.apply_async()
            return jsonify({'result': 'updated'}), 202, {'Location': url_for('taskstatusUpload', task_id=task.id)}
            #proc = Popen(['/home/pi/test/build.sh'], shell=True, stderr=None, stdout=None, stdin=None, close_fds=True)
            #outDict['result'] = True
            #return jsonify(outDict)

        outDict['result']=False    
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
            
            # Write data in Unicode
            f = codecs.open(targetFilePath, 'w+','utf-8')
            f.write( request.json['content'] )
            f.close()
            task = compile_task.apply_async()
            return jsonify({'result': 'updated'}), 202, {'Location': url_for('taskstatus', task_id=task.id)}

@app.route('/', methods=['GET'])
def index_view():
    exampleSelect = ExampleSelectForm()
    return render_template('index.html',
                            exampleSelect=exampleSelect)

@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = compile_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
            response['output'] = task.info['output']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)    

@app.route('/statusUpload/<task_id>')
def taskstatusUpload(task_id):
    task = upload_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
            response['output'] = task.info['output']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response) 

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5002,debug=True)
    #app.run(host="0.0.0.0",port=8080)
