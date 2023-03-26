FROM continuumio/miniconda3:latest

LABEL org.opencontainers.image.source=https://github.com/magsol/countdown-mastobot
LABEL org.opencontainers.image.description="Countdown Mastobot image"
LABEL org.opencontainers.image.licenses=MIT

RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y git && \
    conda update -y --all && \
    conda install -y pip && \
    conda install -c conda-forge python=3.9 mastodon.py && \
    pip install simple_image_download

WORKDIR /opt/

# Check out the scripts.
RUN git clone https://github.com/magsol/countdown-mastobot

# Execute!
RUN cd countdown-mastobot && chmod +x mastobot.sh
CMD ["/bin/bash", "-c", "mastobot.sh"]
