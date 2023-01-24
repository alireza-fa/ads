FROM python:3.9

LABEL MAINTAINER='alireza-fa https://github.com/alireza-fa'

ENV PYTHONUNNUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY . /code

ADD requirements.txt /code

RUN pip install -U pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "--chdir", "A", "--bind", ":8000", "A.wsgi:application"]
