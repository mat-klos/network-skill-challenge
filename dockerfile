FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    postgresql postgresql-contrib \
    python3 python3-pip \
    net-tools iproute2 iputils-ping \
    nmap \
    scapy \
    vim \
    sudo \
    curl \
    && apt-get clean

RUN pip3 install --no-cache-dir --break-system-packages psycopg2-binary pytest pytest-html pytest-json-report python-nmap

WORKDIR /usr/src/app

COPY . .
