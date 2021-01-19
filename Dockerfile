FROM ubuntu:latest
ENV DEBIAN_FRONTEND="noninteractive"
WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app
RUN apt-get -qq update && apt-get -qq install -y tzdata curl aria2 python3 python3-pip \
    locales python3-lxml pv jq ffmpeg p7zip-full p7zip-rar && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY extract /usr/local/bin
RUN chmod +x /usr/local/bin/extract
COPY netrc /root/.netrc
COPY . .
RUN chmod +x aria.sh
RUN locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8' TZ='Asia/Kolkata'
CMD ["bash","start.sh"]
