#!/bin/bash

# Builder script for the image.

docker buildx build \
    --platform linux/arm64,linux/amd64 \
    -t ghcr.io/magsol/countdown_mastobot:latest \
    .
