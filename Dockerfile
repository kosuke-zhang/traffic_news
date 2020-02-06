FROM python:3.7.3

RUN mkdir /project

WORKDIR /project

ADD crawler/. /project

RUN pip install -i https://mirrors.aliyuncs.com/pypi/simple/ -r requirements.txt
