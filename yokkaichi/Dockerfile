FROM alpine:3.19
RUN apk update
RUN apk add python3 py3-pip masscan
WORKDIR /app
COPY . .
RUN pip install --break-system-packages .
CMD ["python", "-m", "yokkaichi", "-v"]
