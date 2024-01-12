FROM alpine:3.19
RUN apk update
RUN apk add python3 nodejs npm
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build
RUN pip install -r requirements.txt --break-system-packages
CMD litestar run
