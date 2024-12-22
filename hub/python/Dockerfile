FROM tensorflow/tensorflow

ENV ESSENTIAL_PACKAGES="ffmpeg libsm6 libxext6" \
    UTILITY_PACKAGES="mlocate sqlite vim"

RUN apt update && \
    apt install -y $ESSENTIAL_PACKAGES $UTILITY_PACKAGES

COPY app/backend/requirements.txt /tmp/requirements.txt
RUN cd /tmp && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

WORKDIR /home/app
