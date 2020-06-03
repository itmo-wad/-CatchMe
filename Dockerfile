FROM python:3.8.1-slim-buster

# set work directory
WORKDIR /usr/comment_cloud/src

# install dependencies
RUN pip install --upgrade pip
COPY ./src/requirements.txt /usr/comment_cloud/src/requirements.txt
RUN pip install -r requirements.txt
