import http.server
import os
import subprocess

PORT = int(os.environ.get("PORT", 8080))

CHECKS = [
    ("whoami/id", ["id"]),
    ("hostname", ["hostname"]),
    ("mounts", ["cat", "/proc/self/mounts"]),
    ("cgroup", ["cat", "/proc/1/cgroup"]),
    ("capabilities (capsh)", ["capsh", "--print"]),
    ("network interfaces", ["ip", "addr"]),
    ("routing table", ["ip", "route"]),
    ("docker.sock present?", ["ls", "-la", "/var/run/docker.sock"]),
    (
        "docker.sock API -> list ALL containers on host",
        [
            "curl", "-s", "--max-time", "5",
            "--unix-socket", "/var/run/docker.sock",
            "http://localhost/containers/json?all=1",
        ],
    ),
    ("/host_root listing", ["ls", "-la", "/host_root"]),
    ("/host_etc listing", ["ls", "-la", "/host_etc"]),
    ("/proc/1/root listing (pid:host artifact)", ["ls", "-la", "/proc/1/root"]),
    ("host process list (pid:host)", ["ps", "aux"]),
    ("/dev listing", ["ls", "-la", "/dev"]),
    ("loaded kernel modules", ["cat", "/proc/modules"]),
]


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        for title, cmd in CHECKS:
            self.wfile.write(f"\n=== {title} ===\n$ {' '.join(cmd)}\n".encode())
            try:
                out = subprocess.run(cmd, capture_output=True, timeout=5)
                self.wfile.write(out.stdout)
                if out.stderr:
                    self.wfile.write(b"[stderr] " + out.stderr + b"\n")
            except FileNotFoundError:
                self.wfile.write(b"[not available in image]\n")
            except Exception as e:
                self.wfile.write(f"[error] {e}\n".encode())

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    print(f"listening on 0.0.0.0:{PORT}", flush=True)
    http.server.HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
