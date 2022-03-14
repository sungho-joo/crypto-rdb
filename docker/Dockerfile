FROM amancevice/pandas:1.4.0-alpine
WORKDIR /usr/app
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip

RUN apk add build-base
RUN apk add --no-cache bash libressl-dev musl-dev libffi-dev
RUN pip install --no-cache-dir -r requirements.txt
