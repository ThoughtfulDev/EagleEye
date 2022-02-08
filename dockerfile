FROM python:3.7-alpine

WORKDIR /app/eagle_eye/

COPY . .

RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub && \
        wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-2.30-r0.apk && \
        wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-bin-2.30-r0.apk && \
        wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux32.tar.gz && \
        apk add --update --no-cache glibc-2.30-r0.apk glibc-bin-2.30-r0.apk firefox g++ make linux-headers cmake \
            libffi-dev gcc python3-dev jpeg-dev zlib-dev && \
        pip3 install --no-cache --upgrade pip setuptools && \
        tar -zxf geckodriver-v0.30.0-linux32.tar.gz -C /usr/bin

RUN pip install -r requirements.txt

ENTRYPOINT ["/app/eagle_eye/entrypoint.sh"]