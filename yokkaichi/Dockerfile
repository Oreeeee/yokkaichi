FROM alpine:3.19
RUN apk update
RUN apk add python3 py3-pip masscan libpcap libpcap-dev
WORKDIR /app
COPY . .
RUN pip install --break-system-packages .
WORKDIR /data
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.12.1/wait /wait
RUN chmod +x /wait
CMD /wait && python -m yokkaichi -c
