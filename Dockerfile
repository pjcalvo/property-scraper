FROM eu.gcr.io/bolcom-stg-baseimages-702/alpine-python:latest

COPY . .

RUN python3 -m pip install -r requirements.txt

CMD python main.py