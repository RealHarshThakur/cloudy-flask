import os
import random
import time
import sys
import requests
from flask import Flask, request, render_template, jsonify, make_response
from flask_restplus import fields, Api, Namespace, Resource,marshal
from flask_mail import Mail, Message
from celery import Celery


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!' 
mail = Mail(app)

api = Api()
# Namespace
email_ns = Namespace('email')

# Model
email_model = email_ns.model('Email details', {
 
    'subject': fields.String(required=True),
    'to': fields.String(required=True),
    'body': fields.String(required=True)
})

api.add_namespace(email_ns)
api.init_app(app)


# Celery configuration

redis_ip = os.environ["REDIS_SERVICE_HOST"]

app.config['CELERY_BROKER_URL'] = "redis://"+redis_ip+":6379"
app.config['CELERY_RESULT_BACKEND'] = "redis://"+redis_ip+":6379"


# Initialize extensions

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def send_email(email_data):
    with app.app_context():    
        requests.post(
            "https://api.mailgun.net/v3/mail.latesttechin.me/messages",
            auth=("api", "Your api key here"), # Use vault
            data={"from": "Excited User <harsh@mail.latesttechin.me>",
                "to": email_data['to'],
                "subject": email_data['subject'],
                "text": email_data['body']})

@email_ns.route('/')
class Email(Resource):
    @email_ns.doc('Used to send emails')
    @email_ns.expect(email_model)
    def post(self):
        
        subject = email_ns.payload['subject']
        to = email_ns.payload['to']
        body = email_ns.payload['body']
        
        email_data = {
        'subject': subject,
        'to': to,
        'body': body}

        try:
            send_email.delay(email_data)
            return make_response(jsonify("Msg: Email sent",200))
        except:
            print(sys.exc_info())
            return make_response(jsonify("msg: error"),500)
