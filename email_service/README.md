# Email Service

I've used mailgun's API to send out emails. Primary purpose of writing this service was to explore how to use Celery and Redis in a messaging system.
If you'd like to use SMTP credentials, you can look at this repo : https://github.com/miguelgrinberg/flask-celery-example/

To start this service, run :
- kubectl create -f email.yaml
