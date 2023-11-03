FROM python:3.12-alpine

# create the app user
RUN addgroup --system app
RUN adduser --ingroup app --disabled-password app

# create directory for the app user
RUN mkdir -p /home/app/bot
WORKDIR /home/app/bot

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project
COPY . .

# install system dependencies
RUN apk update
RUN apk add build-base python3-dev gcc musl-dev
RUN apk add --upgrade netcat-openbsd

# install python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# lint
RUN pip install flake8==6.0.0
RUN flake8 --ignore=E501,F401,F541 ./

# chown all the files to the app user
RUN chown -R app:app /home/app/bot

# change to the app user
USER app
