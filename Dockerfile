FROM python:3.10.4-slim-buster

RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends ffmpeg aria2 python3-pip \
    && apt-get clean \
    && apt-get install -y wget python3-dev mediainfo \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/
RUN pip3 install --no-cache-dir --upgrade --requirement requirements.Watermark
CMD python3 -m Watermark
