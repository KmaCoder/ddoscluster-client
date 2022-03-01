FROM python:3.10

LABEL Maintainer="maxim4110@gmail.com"

WORKDIR /usr/app/src
COPY . ./

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "./main.py"]