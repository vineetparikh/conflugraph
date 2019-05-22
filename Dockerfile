FROM python:2.7-alpine

ADD confluence-graph.py /conflu/
ADD requirements.txt /conflu/
WORKDIR /conflu
RUN su -H pip install -r requirements.txt
