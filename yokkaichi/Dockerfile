FROM alpine:3.19
RUN apk update
RUN apk add python3 py3-pip masscan libpcap libpcap-dev
WORKDIR /app
COPY . .
RUN pip install --break-system-packages .
WORKDIR /data
CMD ["python", "-m", "yokkaichi", "-c"]
