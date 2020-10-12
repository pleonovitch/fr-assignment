FROM alpine:3.11
COPY requirements.txt /
RUN apk add --update --no-cache graphviz \
            ttf-freefont

ENV PYTHONUNBUFFERED=1
RUN echo "**** install Python3 ****" && \
    apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi
RUN pip3 install virtualenv
RUN pip3 install -r /requirements.txt
