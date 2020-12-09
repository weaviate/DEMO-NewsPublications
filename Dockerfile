FROM alpine:3.10.2

ENV weaviate_host="http://localhost:8080"
ENV cache_dir="cache-en"
ENV batch_size="200"

RUN apk add --no-cache build-base python3-dev python3 py3-pillow py3-lxml g++ make git bash curl && \
    pip3 install --upgrade pip

ENV LIBRARY_PATH=/lib:/usr/lib

RUN mkdir -p /root/DEMO-NewsPublications && \
    cd /root/DEMO-NewsPublications

COPY . /root/DEMO-NewsPublications

RUN cd /root/DEMO-NewsPublications && \
    pip3 install -r requirements.txt && \
    chmod +x /root/DEMO-NewsPublications/import.sh

#ENTRYPOINT ["/bin/bash"]
CMD /root/DEMO-NewsPublications/import.sh ${weaviate_host} ${cache_dir} ${batch_size}