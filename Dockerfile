FROM ubuntu
ARG S6_OVERLAY_VERSION=3.1.5.0

ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-aarch64.tar.xz /tmp
RUN apt-get update && apt-get install --no-install-recommends -y \
        xz-utils && \
        tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz && \
        tar -C / -Jxpf /tmp/s6-overlay-aarch64.tar.xz

# Install dependencies
RUN apt-get update && apt-get install -y python3 && python3 -v &&  apt-get install -y python3-pip
# Copy application
RUN mkdir -p /app
COPY server.py /app
COPY requirements.txt /app
# RUN echo $(ls -1 /app/)
# RUN echo $(pwd /app)
# Setup python dependencies
RUN pip3 install -r /app/requirements.txt

CMD ["python3","/app/server.py"]
EXPOSE 8080
EXPOSE 8765

ENTRYPOINT [ "/init" ]
