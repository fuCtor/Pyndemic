FROM python:3.6-alpine
RUN mkdir /app
WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . .

ENTRYPOINT python pyndemic.py