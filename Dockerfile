FROM ubuntu:latest

RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends ffmpeg aria2 python3-pip \
    && apt-get clean \
    && apt-get install -y wget python3-dev mediainfo \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/
RUN pip3 install --no-cache-dir --upgrade --requirement requirements.txt
CMD python3 -m Downloader
