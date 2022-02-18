FROM python:3.9-slim
COPY . /src
RUN PIP_NO_CACHE_DIR=1 pip install /src && rm -rf /src
ENTRYPOINT ["gcn-classic-to-kafka"]
USER nobody:nogroup
