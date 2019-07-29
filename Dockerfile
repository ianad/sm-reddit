FROM jupyter/datascience-notebook:latest

USER root

RUN apt-get update

COPY init init
COPY work work

RUN pip install --no-cache -r init/requirements.txt