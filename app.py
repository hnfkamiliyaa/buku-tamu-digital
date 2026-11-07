from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import urllib.parse

DATA_FILE = "guestbook.json"

def load_messages():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_messages(messages):
    temp_file = DATA_FILE + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
    os.replace(temp_file, DATA_FILE)

class GuestbookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)

        if path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy"}).encode("utf-8"))
            return

        if path == "/messages":
            messages = load_messages()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(messages).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == "/messages":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode("utf-8"))
                name = data.get("name", "").strip()
                message = data.get("message", "").strip()

                if not name or not message:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Nama dan pesan wajib diisi"}).encode("utf-8"))
                    return

                messages = load_messages()
                messages.append({"name": name, "message": message})
                save_messages(messages)

                self.send_response(201)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

    def do_DELETE(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == "/messages":
            query = urllib.parse.parse_qs(parsed_path.query)
            if "index" in query:
                try:
                    idx = int(query["index"][0])
                    messages = load_messages()
                    if 0 <= idx < len(messages):
                        messages.pop(idx)
                        save_messages(messages)
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json; charset=utf-8")
                        self.end_headers()
                        self.wfile.write(json.dumps({"status": "deleted"}).encode("utf-8"))
                        return
                except ValueError:
                    pass
            self.send_response(400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Indeks tidak valid"}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

def run(server_class=HTTPServer, handler_class=GuestbookHandler, port=5000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Server backend berjalan pada port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()