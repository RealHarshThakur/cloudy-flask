FROM python  
COPY . /user_service/
WORKDIR /user_service
RUN apt install python3 && python3 -m pip install flask-restplus flask-bcrypt validate-email requests
ENV FLASK_APP=user_manager.py
ENTRYPOINT [ "flask" ,"run","--host=0.0.0.0"]

