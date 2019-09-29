FROM python:3.7.1
WORKDIR /code
ADD requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple
ADD . .
CMD ["python", "send.py"]