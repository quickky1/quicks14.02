import http.server, os

ROOT = "/home/mc/ag1402"
LOG = os.path.join(ROOT, "serve.log")


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        super().end_headers()

    def log_message(self, fmt, *args):
        try:
            with open(LOG, "a") as f:
                f.write(self.address_string() + " " + (fmt % args) + "\n")
        except Exception:
            pass

    def do_GET(self):
        if self.path.startswith("/ag_log"):
            self.send_response(200)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        super().do_GET()


http.server.ThreadingHTTPServer(("0.0.0.0", 1337), H).serve_forever()
