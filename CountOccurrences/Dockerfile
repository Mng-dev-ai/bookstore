FROM python:3.8

RUN mkdir /code
WORKDIR /code

COPY requirements.txt ./
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY CountOccurrences CountOccurrences/
EXPOSE 5001