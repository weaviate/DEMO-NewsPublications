FROM alpine:3.10.2

ENV weaviate_host "http://localhost:8080"
ARG weaviate_host=${weaviate_host}

RUN apk add --no-cache build-base python-dev python3 py3-pillow py3-lxml g++ make git bash && \
    pip3 install --upgrade pip

ENV LIBRARY_PATH=/lib:/usr/lib

RUN cd /root && \
    git clone --depth=1 https://github.com/semi-technologies/weaviate-cli && \
    cd weaviate-cli && \
    pip3 install -r requirements.txt && \
    ln -s $(pwd)/bin/weaviate-cli /usr/local/bin/weaviate-cli

RUN mkdir -p /root/DEMO-NewsPublications && \
    cd /root/DEMO-NewsPublications

COPY . /root/DEMO-NewsPublications

RUN cd /root/DEMO-NewsPublications && \
    pip3 install -r requirements.txt && \
    chmod +x /root/DEMO-NewsPublications/import.sh

#ENTRYPOINT ["/bin/bash"]
CMD /root/DEMO-NewsPublications/import.sh ${weaviate_host}