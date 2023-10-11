FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y openssh-server sshpass

RUN apt-get clean

WORKDIR /usr/src/

COPY ./requirements.txt .

RUN pip install -r requirements.txt

RUN rm requirements.txt

# COMPILACION
COPY ./app.py ./
COPY ./apps ./apps
COPY ./files ./files

ENTRYPOINT ["python","app.py"]