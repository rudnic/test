FROM alpine:3.19

RUN apk add --no-cache python3 curl iproute2 libcap procps

COPY server.py /app/
WORKDIR /app

EXPOSE 8080
ENV PORT=8080

CMD ["python3", "server.py"]
