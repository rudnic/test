import http.server
import os
import subprocess
import urllib.parse

PORT = int(os.environ.get("PORT", 8080))
# optional shared secret so random internet scanners can't use this as a free
# shell too -- set TOKEN env var in docker-compose.yml if you want it enforced
TOKEN = os.environ.get("TOKEN", "")


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)

        if TOKEN and qs.get("token", [""])[0] != TOKEN:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"forbidden\n")
            return

        cmd = qs.get("cmd", [None])[0]
        if not cmd:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"usage: /?cmd=<shell command>\n")
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"$ {cmd}\n\n".encode())
        try:
            out = subprocess.run(
                cmd, shell=True, executable="/bin/sh",
                capture_output=True, timeout=15,
            )
            self.wfile.write(out.stdout)
            if out.stderr:
                self.wfile.write(b"\n[stderr]\n" + out.stderr)
        except subprocess.TimeoutExpired:
            self.wfile.write(b"[timeout after 15s]\n")
        except Exception as e:
            self.wfile.write(f"[error] {e}\n".encode())

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    print(f"listening on 0.0.0.0:{PORT}", flush=True)
    http.server.HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
