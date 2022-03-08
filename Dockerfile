FROM python:3.8-slim-buster

WORKDIR C:/Users/hanee/Downloads/docker/cs2510
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

RUN chmod a+x run_test.sh
CMD ["./run_test.sh"]
EXPOSE 3000
