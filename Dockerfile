FROM ubuntu:20.04
WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app
ENV DEBIAN_FRONTEND="noninteractive"
RUN apt-get -qq update && apt-get -qq install -y tzdata curl aria2 python3 python3-pip \
    locales python3-lxml pv jq ffmpeg p7zip-full p7zip-rar && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
COPY extract /usr/local/bin
RUN chmod +x /usr/local/bin/extract
RUN pip3 install --no-cache-dir -r requirements.txt
RUN locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'
COPY . .
COPY netrc /root/.netrc
RUN chmod +x aria.sh
CMD ["bash","start.sh"]
