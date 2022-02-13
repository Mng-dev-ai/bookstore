FROM python:3.8

RUN mkdir /code
WORKDIR /code

COPY requirements.txt setup.py tox.ini ./
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install -e .

RUN apt-get update && apt-get install -y default-mysql-client

COPY BookStore BookStore/
COPY entrypoint.sh entrypoint.sh
COPY migrations migrations/

RUN chmod u+x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
EXPOSE 5000     