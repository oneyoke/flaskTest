#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, abort, jsonify, url_for, session
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

import uuid

# Google calendar
import httplib2
import os
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import datetime
import time
import threading
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
eventsList = []
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def calendar_update():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    
    threading.Timer(20, calendar_update).start()

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #print('Getting the upcoming 10 events')
    eventsResult = service.events().list(calendarId='h35rg8ljcle23h1s2to16b9g2k@group.calendar.google.com', timeMin=now, maxResults=10, singleEvents=True,orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    #import pdb; pdb.set_trace()
    if not events:
        print('No upcoming events found.')
    global eventsList
    eventsList = []   #Think about
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        startepoch = time.mktime(time.strptime(event['start']['dateTime'][:19],'%Y-%m-%dT%H:%M:%S'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        endepoch = time.mktime(time.strptime(event['end']['dateTime'][:19],'%Y-%m-%dT%H:%M:%S'))
        #print(start, end, event['summary'])
        eventsList += [(startepoch, endepoch, event['summary'])]

    #print(eventsList)
    print 'is_occupied: ' + str(is_occupied())   

def is_occupied():
    #threading.Timer(5, is_occupied).start()
    global eventsList
    now = time.time()
    for event in eventsList:
        if now > event[0] and now < event[1]:
            print(event[0], event[1], event[2])
            #print(True)
            return True
    #print(False)        
    return False



app = Flask(__name__)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task(bind=True)
def compile_task(self,user_id):
    self.update_state(state='PROGRESS',
                          meta={'current': 0, 'total': 1,
                                'status': 'message'})
    print(user_id)
    process = subprocess.Popen(['/home/pi/test/only_build.sh',user_id],
                                shell=False,
                                stderr=subprocess.STDOUT,
                                stdout=subprocess.PIPE,
                                stdin=None,
                                close_fds=True)
    output = process.communicate()[0] 

    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42, 'output': output}

@celery.task(bind=True)
def upload_task(self,user_id):
    print(user_id)
    self.update_state(state='PROGRESS',
                          meta={'current': 0, 'total': 1,
                                'status': 'message'})
    process = subprocess.Popen(['/home/pi/test/only_upload.sh',user_id],
                                shell=False,
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
            #user_id = request.args.get('user_id')
            if is_occupied():
                print("Occupied")
                return jsonify({'result': 'occupied'})    
            user_id = session['username']
            task = upload_task.apply_async([user_id])
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
            #f = codecs.open(targetFilePath, 'w+','utf-8')
            #user_id = request.json['user_id']
            if is_occupied():
                print('Occupied')
                return jsonify({'result': 'occupied'})
            user_id = session['username']
            f = codecs.open('userino/'+user_id+'.ino', 'w+','utf-8')
            f.write( request.json['content'] )
            f.close()
           
            task = compile_task.apply_async([user_id])
            return jsonify({'result': 'updated'}), 202, {'Location': url_for('taskstatus', task_id=task.id)}

@app.route('/', methods=['GET'])
def index_view():
    exampleSelect = ExampleSelectForm()
    if 'username' not in session:
        session['username'] = str(uuid.uuid4())
    print session['username']    
    return render_template('index.html',
                            exampleSelect=exampleSelect,
                            user_id = uuid.uuid4())

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
    #app.run(host="0.0.0.0",port=5002,debug=True)
    t1 = threading.Timer(5, calendar_update)
    #t2 = threading.Timer(6, is_occupied)
    t1.start()
    #t2.start()
    app.run(host="0.0.0.0",port=8080)
