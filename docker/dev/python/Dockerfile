FROM python:3.6.5
MAINTAINER Tianchen@cuhk

COPY . /orwell

WORKDIR /orwell

RUN pip install -r requirements/dev.txt

CMD ["python","manage.py","runserver","0.0.0.0:8000","--settings=orwell.settings.local"]