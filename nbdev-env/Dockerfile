FROM python:3.10.6-slim-bullseye

ARG GID=1000
ARG UID=1000

RUN addgroup --gid=$GID loper && adduser --uid=$UID --gid=$GID loper && \
    apt-get update && apt-get install -y --no-install-recommends curl git && \
    ln -sf /usr/share/zoneinfo/America/Chicago /etc/localtime && \
    rm -rf /var/lib/apt/lists/*
RUN curl -LO https://www.quarto.org/download/latest/quarto-linux-amd64.deb && \
    dpkg -i *64.deb && rm *64.deb

USER loper
ENV HOME=/home/loper
ENV PATH=$HOME/.local/bin:$PATH
ENV PIP_CACHE_DIR=$HOME/.cache/pip

WORKDIR /home/loper
COPY --chown=$GID:$UID ./nbdev-env/requirements.txt requirements.txt

SHELL ["/bin/bash", "-c"]

RUN pip install --user --upgrade pip && \
    pip install --user --upgrade --requirement requirements.txt

VOLUME /home/loper

CMD ["env"]
