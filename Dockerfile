FROM ubuntu:latest
ENV DEBIAN_FRONTEND='noninteractive'
RUN apt-get -qq update && apt-get -qq install -y tzdata curl aria2 python3 python3-pip \
    locales python3-lxml pv jq nano ffmpeg p7zip-full p7zip-rar && rm -rf /var/lib/apt/lists/*
WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app
COPY . .
RUN python3 setup.py bdist_wheel && cd dist && pip3 install --no-cache-dir tgmb-*.whl
RUN locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8' TZ='Asia/Kolkata' MEGA_SDK_VERSION='3.8.1'
CMD ["python3", "-m", "tgmb"]
# MEGA SUPPORT
RUN apt-get -qq update && apt-get -qq install -y --no-install-recommends software-properties-common && \
    add-apt-repository ppa:rock-core/qt4 && apt-get -qq install -y --no-install-recommends git g++ gcc autoconf make \
    automake libtool m4 qt4-qmake libqt4-dev libcurl4-openssl-dev libcrypto++-dev libsqlite3-dev libc-ares-dev \
    libsodium-dev libnautilus-extension-dev libssl-dev libfreeimage-dev swig && apt-get -y autoremove
RUN git clone https://github.com/meganz/sdk.git sdk && cd sdk && git checkout v$MEGA_SDK_VERSION && \
    ./autogen.sh && ./configure --disable-silent-rules --enable-python --with-sodium --disable-examples && \
    make -j$(nproc --all) && cd bindings/python && python3 setup.py bdist_wheel && cd dist && \
    pip3 install --no-cache-dir megasdk-$MEGA_SDK_VERSION-*.whl
