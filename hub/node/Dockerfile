FROM node:alpine3.20

ENV ESSENTIAL_PACKAGES="" \
    UTILITY_PACKAGES="mlocate vim"

RUN apk update && \
    apk --no-cache --progress add $ESSENTIAL_PACKAGES $UTILITY_PACKAGES

WORKDIR /home/app
