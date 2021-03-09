FROM python:3.9.2-slim-buster
LABEL maintainer="stefan@hagen.link" version="0.0.1" st.efan.hagen.vendor="Stefan Hagen" 
RUN export DEBIAN_FRONTEND=noninteractive && \
apt-get update && \
apt-get install -y --no-install-recommends tini && \
apt-get -y clean && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade --no-cache-dir pip && pip install --no-cache-dir -r requirements.txt
RUN useradd --create-home action
USER action
COPY csaf_lint /app
ENV PYTHONFAULTHANDLER=1
ENTRYPOINT ["tini", "--", "python", "-m", "csaf_lint"]
