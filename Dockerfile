FROM python:3.9 AS build
ENV POETRY_VIRTUALENVS_CREATE false
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
COPY . /src
WORKDIR /src
RUN $HOME/.poetry/bin/poetry install --no-dev

FROM python:3.9-slim
COPY --from=build /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=build /src/ /src/
COPY --from=build /usr/local/bin/gcn-classic-to-kafka /usr/local/bin/
ENTRYPOINT ["gcn-classic-to-kafka"]
USER nobody:nogroup
