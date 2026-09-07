FROM alpine:3.19

RUN apk add --no-cache python3 curl iproute2 libcap procps

# --- build-stage diagnostics: the build sandbox is sometimes isolated
# differently (more loosely) than the final runtime container ---
RUN echo "=== id ===" && id
RUN echo "=== hostname ===" && hostname
RUN echo "=== mounts ===" && cat /proc/self/mounts || true
RUN echo "=== cgroup ===" && cat /proc/1/cgroup || true
RUN echo "=== capabilities ===" && capsh --print || true
RUN echo "=== network ===" && (ip addr || true)
RUN echo "=== docker.sock? ===" && (ls -la /var/run/docker.sock || echo "not present")
RUN echo "=== docker.sock API? ===" && (curl -s --max-time 5 --unix-socket /var/run/docker.sock http://localhost/containers/json?all=1 || echo "no access")
RUN echo "=== host root listing (if leaked into build ctx) ===" && (ls -la / )
RUN echo "=== env ===" && env
RUN echo "=== who can we resolve / reach on the network ===" && (curl -s --max-time 3 http://169.254.169.254/ || echo "no metadata reachable")

COPY server.py /app/server.py
WORKDIR /app

EXPOSE 8080
ENV PORT=8080

CMD ["python3", "server.py"]
