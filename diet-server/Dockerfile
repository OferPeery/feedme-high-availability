FROM python:alpine3.17

WORKDIR ./diet-server

COPY ./* .

RUN pip install requests

RUN pip install flask

RUN pip install flask_restful

RUN pip install pymongo

ENV FLASK_APP=main.py

ENV FLASK_RUN_HOST=0.0.0.0

ENV FLASK_RUN_PORT=8002

EXPOSE 8002

CMD ["flask", "run"]