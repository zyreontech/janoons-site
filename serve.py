#!/usr/bin/env python3
"""Local dev server for janoons.com — mimics static-host behaviour.
  python3 serve.py [port]      (default 8799)
- Serves files from this directory
- /gov.html -> 301 /government.html (as in _redirects)
- Missing paths -> 404.html with a real 404 status
- POST to the contact form -> logs the fields and redirects to /thanks.html
"""
import http.server, os, sys, urllib.parse, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8799
REDIRECTS = {"/gov.html": "/government.html", "/index.html": "/"}

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def do_GET(self):
        path = urllib.parse.urlsplit(self.path).path
        if path in REDIRECTS:
            self.send_response(301); self.send_header("Location", REDIRECTS[path]); self.end_headers(); return
        if path.startswith("/_") or path == "/serve.py":
            return self.send_404()
        fs = os.path.join(ROOT, path.lstrip("/"))
        if not os.path.exists(fs):
            return self.send_404()
        super().do_GET()

    def send_404(self):
        body = open(os.path.join(ROOT, "404.html"), "rb").read()
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = urllib.parse.parse_qs(self.rfile.read(length).decode())
        fields = {k: v[0] for k, v in data.items() if k not in ("form-name", "company")}
        stamp = datetime.datetime.now().isoformat(timespec="seconds")
        line = f"{stamp} {fields}\n"
        with open(os.path.join(ROOT, "_submissions.log"), "a") as f:
            f.write(line)
        print("FORM SUBMISSION", line.strip(), flush=True)
        self.send_response(303); self.send_header("Location", "/thanks.html"); self.end_headers()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

if __name__ == "__main__":
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    with http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler) as srv:
        print(f"janoons.com dev server → http://localhost:{PORT}/   (Ctrl-C to stop)", flush=True)
        srv.serve_forever()
