flask run --host=0.0.0.0 --port=7000&  
celery worker -A app.celery --loglevel=info
