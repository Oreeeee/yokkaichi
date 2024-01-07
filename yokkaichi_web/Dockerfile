FROM alpine:3.19
RUN apk update
RUN apk add python3
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt --break-system-packages
CMD litestar run
