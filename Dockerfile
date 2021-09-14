FROM daocloud.io/python:3-onbuild
WORKDIR /opt/flask_demo

RUN pip install --upgrade pip
RUN pip list
COPY requirements/linux.txt ./
RUN pip install -r linux.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

COPY run.py ./

COPY gunicorn.py ./

CMD ["gunicorn", "run:app", "-c", "./gunicorn.py"]
