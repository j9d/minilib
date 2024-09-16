FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

RUN apt update && apt full-upgrade -y
RUN apt install -y \
    uwsgi \
    uwsgi-plugin-python3

RUN mkdir /opt/minilib /opt/static

WORKDIR /opt/minilib

COPY . /opt/minilib/

RUN uv sync --frozen --no-dev

CMD ["sh", "start.sh"]
