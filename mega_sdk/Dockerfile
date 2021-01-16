FROM python:3-slim-buster
RUN apt-get -qq update && apt-get -qq install -y git g++ gcc autoconf automake m4 libtool qt4-qmake make libqt4-dev \
    libcurl4-openssl-dev libcrypto++-dev libsqlite3-dev libc-ares-dev libsodium-dev libnautilus-extension-dev swig \
    libssl-dev libfreeimage-dev software-properties-common && rm -rf /var/lib/apt/lists/*
ENV MEGA_SDK_VERSION '3.7.9'
RUN git clone https://github.com/meganz/sdk.git sdk && cd sdk && git checkout v$MEGA_SDK_VERSION && ./autogen.sh && \
    ./configure --disable-silent-rules --enable-python --disable-examples && make -j$(nproc --all) && cd bindings/python/ && \
    python3 setup.py bdist_wheel && cd dist/ && pip3 install --no-cache-dir megasdk-$MEGA_SDK_VERSION-*.whl
