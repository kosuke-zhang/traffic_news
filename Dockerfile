FROM python:3.7.3

RUN mkdir /project

WORKDIR /project

ADD crawler/. /project

RUN mkdir error log

RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
