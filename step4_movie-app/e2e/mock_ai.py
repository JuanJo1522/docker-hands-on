from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class RecommendationHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        response = json.dumps({
            "category": payload.get("category"),
            "recommendation": "The Shawshank Redemption: una historia emotiva sobre la esperanza.",
            "model": "e2e-mock",
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, *_args):
        pass


HTTPServer(("0.0.0.0", 8000), RecommendationHandler).serve_forever()
