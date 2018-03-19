# FROM python:3.4-alpine
# ADD . /code
# WORKDIR /code
# RUN pip install -r requirements.txt
# CMD ["python", "app.py"]

FROM ubuntu:latest
MAINTAINER Rajdeep Dua "dua_rajdeep@yahoo.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]