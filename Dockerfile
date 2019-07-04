FROM python:2.7
ADD confluence-graph.py /conflu/
ADD requirements.txt /conflu/
WORKDIR /conflu
RUN pip install -r requirements.txt
