FROM continuumio/miniconda3:latest

LABEL org.opencontainers.image.source=https://github.com/magsol/countdown-mastobot
LABEL org.opencontainers.image.description="Countdown Mastobot image"
LABEL org.opencontainers.image.licenses=MIT

RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y git && \
    conda update -y --all && \
    conda install -y pip && \
    conda install -c conda-forge python=3.9 mastodon.py=1.8.0 && \
    pip install simple_image_download==0.5

RUN mkdir /app && cd /app && \
    git clone https://github.com/magsol/countdown-mastobot && \
    cd countdown-mastobot && chmod +x mastobot.sh

# Keep us here.
WORKDIR /app/countdown-mastobot

# Execute!
CMD ["/bin/bash", "-c", "mastobot.sh"]
