FROM ubuntu:latest
ENV DEBIAN_FRONTEND='noninteractive'
RUN apt-get -qq update && apt-get -qq install -y tzdata curl aria2 python3 python3-pip \
    locales python3-lxml pv jq nano ffmpeg p7zip-full p7zip-rar && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir tgmb
RUN locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8' TZ='Asia/Kolkata'
WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app
CMD ["python3", "-m", "tgmb"]
