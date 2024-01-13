FROM ubuntu:latest

RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends gcc g++ libffi-dev musl-dev ffmpeg aria2 python3-pip \
    && apt-get clean \
    && apt-get install -y curl git wget pv jq python3-dev mediainfo \
    && git clone https://github.com/axiomatic-systems/Bento4.git \
    && cd Bento4 \
    && apt-get install -y cmake \
    && mkdir cmakebuild \
    && cd cmakebuild/ \
    && cmake -DCMAKE_BUILD_TYPE=Release .. \
    && make \
    && make install \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/
RUN pip3 install wheel
RUN pip3 install --no-cache-dir --upgrade --requirement requirements.txt
CMD python3 -m Downloader
