FROM python  AS base
RUN apt install python3 && python3 -m pip install flask-restplus flask-bcrypt validate-email requests flask-jwt-extended

FROM base
COPY . /user_service/
WORKDIR /user_service
ENV FLASK_APP=user_manager.py
ENTRYPOINT [ "flask" ,"run","--host=0.0.0.0","--port=8000"]

