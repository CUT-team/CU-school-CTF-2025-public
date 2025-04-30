FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y wget build-essential libssl-dev libffi-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev libncurses5-dev libgdbm-dev \
    liblzma-dev uuid-dev socat

RUN wget https://www.python.org/ftp/python/3.7.17/Python-3.7.17.tgz && \
    tar xzf Python-3.7.17.tgz && \
    cd Python-3.7.17 && \
    ./configure --prefix=/opt/python3.7-custom && \
    make CFLAGS="-DPy_HASH_CUTOFF=7" -j4 && make install && \
    cd .. && rm -rf Python-3.7.17 Python-3.7.17.tgz

ENV PATH="/opt/python3.7-custom/bin:${PATH}"

COPY app.py .
COPY run.sh .

RUN chmod +x run.sh

EXPOSE 31337
CMD ["./run.sh"]