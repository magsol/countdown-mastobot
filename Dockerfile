FROM mambaorg/micromamba:1.4.0-bullseye-slim

LABEL org.opencontainers.image.source=https://github.com/magsol/countdown-mastobot
LABEL org.opencontainers.image.description="Countdown Mastobot image"
LABEL org.opencontainers.image.licenses=MIT

USER root

# First, upgrade the OS.
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y libmagic1 git vim

USER $MAMBA_USER
WORKDIR /tmp

# Next, check out the repo.
RUN git clone https://github.com/magsol/countdown-mastobot
WORKDIR /tmp/countdown-mastobot
RUN chmod +x mastobot.sh
ENV PIP_NO_DEPS=1

# Next, follow instructions here:
# https://hub.docker.com/r/mambaorg/micromamba#quick-start
RUN micromamba install -y -n base -f environment.yml && \
    micromamba clean --all --yes

# Execute!
CMD ["/bin/bash", "mastobot.sh"]
