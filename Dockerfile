FROM python:3.7.3

RUN mkdir /project

WORKDIR /project

ADD crawler/. /project

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
