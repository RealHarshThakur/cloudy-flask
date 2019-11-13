FROM alpine 
COPY . /database/
WORKDIR /database
RUN apk add python3 && python3 -m pip install -r requirements.txt 
ENV FLASK_APP=database.py
ENTRYPOINT [ "flask" ,"run","--host=0.0.0.0"]








