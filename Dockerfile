FROM python:3.9.4-slim-buster
RUN export DEBIAN_FRONTEND=noninteractive && \
apt-get update && \
apt-get -y upgrade && \
apt-get install -y --no-install-recommends tini && \
apt-get -y clean && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade --no-cache-dir pip && pip install --no-cache-dir -r requirements.txt
RUN useradd --create-home action
USER action
COPY csaf_lint /app/csaf_lint
ENV PYTHONFAULTHANDLER=1
ENTRYPOINT ["tini", "--", "python", "-m", "csaf_lint"]
ARG BUILD_TS
ARG REVISION
ARG VERSION
LABEL org.opencontainers.image.created=$BUILD_TS \
    org.opencontainers.image.authors="Stefan Hagen <mailto:stefan@hagen.link>" \
    org.opencontainers.image.url="https://hub.docker.com/repository/docker/shagen/csaf-lint/" \
    org.opencontainers.image.documentation="https://sthagen.github.io/fluffy-funicular/" \
    org.opencontainers.image.source="https://github.com/sthagen/fluffy-funicular/" \
    org.opencontainers.image.version=$VERSION \
    org.opencontainers.image.revision=$REVISION \
    org.opencontainers.image.vendor="Stefan Hagen <mailto:stefan@hagen.link>" \
    org.opencontainers.image.licenses="MIT License" \
    org.opencontainers.image.ref.name="shagen/csaf-lint" \
    org.opencontainers.image.title="csaf-lint." \
    org.opencontainers.image.description="Experimental CSAF envelope and body profile validator."
