FROM amancevice/pandas:1.4.0-alpine
WORKDIR /usr/app
COPY requirements.txt requirements.txt
ADD ./src /usr/app/src
RUN pip install --upgrade pip

RUN apk add build-base
RUN apk add --no-cache bash libressl-dev musl-dev libffi-dev
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/usr/app/src"
ENTRYPOINT ["python3", "./src/websocket/insert_data.py"]
