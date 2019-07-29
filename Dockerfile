FROM jupyter/datascience-notebook:latest

RUN apt-get update

COPY requirements.txt requirements.txt

RUN pip install --no-cache -r requirements.txt