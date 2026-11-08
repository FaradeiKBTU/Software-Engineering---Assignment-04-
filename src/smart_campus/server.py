"""Thin HTTP/UI layer (stdlib only). No rules here - it just calls RoomService."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .service import RoomService

STATIC = os.path.join(os.path.dirname(__file__), "..", "..", "static")
TYPES = {".html": "text/html", ".js": "text/javascript", ".css": "text/css"}


def make_handler(service):
    class Handler(BaseHTTPRequestHandler):
        def _send(self, code, body, ctype="application/json"):
            data = body if isinstance(body, bytes) else json.dumps(body).encode()
            self.send_response(code)
            self.send_header("Content-Type", ctype + "; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            url = urlparse(self.path)
            q = parse_qs(url.query)
            if url.path == "/api/config":
                return self._send(200, service.config())
            if url.path == "/api/rooms":
                eq = [e for e in q.get("equipment", [""])[0].split(",") if e]
                return self._send(200, service.search(q.get("participants", [""])[0], eq))
            name = "index.html" if url.path == "/" else url.path.lstrip("/")
            path = os.path.normpath(os.path.join(STATIC, name))
            if not path.startswith(os.path.normpath(STATIC)) or not os.path.isfile(path):
                return self._send(404, {"error": "not found"})
            with open(path, "rb") as f:
                self._send(200, f.read(), TYPES.get(os.path.splitext(path)[1], "text/plain"))

        def do_POST(self):
            if urlparse(self.path).path != "/api/check":
                return self._send(404, {"error": "not found"})
            try:
                n = int(self.headers.get("Content-Length", 0))
                body = json.loads(self.rfile.read(n) or b"{}")
            except ValueError:
                return self._send(400, {"error": "bad json"})
            self._send(200, service.check(body.get("room"), body.get("start"), body.get("end")))

        def log_message(self, *a):
            pass
    return Handler


def create_server(port=8000, service=None):
    return ThreadingHTTPServer(("127.0.0.1", port), make_handler(service or RoomService()))


if __name__ == "__main__":
    srv = create_server(8000)
    print("Open http://127.0.0.1:8000")
    srv.serve_forever()
