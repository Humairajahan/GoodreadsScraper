FROM python:3.10

WORKDIR /codebase

COPY requirements.txt /codebase/requirements.txt

RUN pip install --upgrade pip \
  && pip install --trusted-host pypi.python.org -r /codebase/requirements.txt 

COPY ./api /codebase/api