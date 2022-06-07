FROM amancevice/pandas:1.4.0-alpine
WORKDIR /usr/app
RUN pip install --upgrade pip

RUN apk add build-base
RUN apk add --no-cache bash libressl-dev musl-dev libffi-dev tmux vim libpq-dev python3-dev
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
