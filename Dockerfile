FROM python:3.9-alpine

ENV weaviate_host="http://localhost:8080"
ENV cache_dir="cache-en"
ENV batch_size="200"

RUN apk add --update --no-cache g++ gcc libxslt-dev jpeg-dev && \
    pip3 install --upgrade pip

RUN mkdir -p /root/DEMO-NewsPublications 

WORKDIR /root/DEMO-NewsPublications

COPY . .

RUN pip3 install -r requirements.txt 

CMD python import.py ${weaviate_host} ${cache_dir} ${batch_size}