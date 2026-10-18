#!/usr/bin/env python3
import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

PORT = 5051
STORAGE_FILE = "/home/samrat/news24/saved_articles.json"
EXPORT_FILE = "/home/samrat/news24/news_for_notebooklm.md"

def load_saved():
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_articles(articles):
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    
    # Also update export markdown for NotebookLM
    with open(EXPORT_FILE, "w", encoding="utf-8") as f:
        f.write("# News24 Saved Articles — Ready for NotebookLM Deep Dive\n\n")
        f.write(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n---\n\n")
        for i, a in enumerate(articles, 1):
            f.write(f"### {i}. {a.get('title', 'Untitled')}\n")
            f.write(f"- **Source**: {a.get('source', 'Unknown')}\n")
            f.write(f"- **Link**: {a.get('url', '')}\n")
            f.write(f"- **Saved At**: {a.get('saved_at', '')}\n")
            if a.get('snippet'):
                f.write(f"- **Summary**: {a.get('snippet')}\n")
            f.write("\n---\n\n")

class NewsAPIHandler(BaseHTTPRequestHandler):
    def _send_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors()
        self.end_headers()

    def do_POST(self):
        if self.path == "/save-article":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body)
                title = data.get("title", "Untitled")
                url = data.get("url", "")
                source = data.get("source", "Unknown")
                snippet = data.get("snippet", "")
                
                articles = load_saved()
                
                # Check if already saved
                existing = [a for a in articles if a.get("url") == url]
                if not existing:
                    new_item = {
                        "title": title,
                        "url": url,
                        "source": source,
                        "snippet": snippet,
                        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    articles.insert(0, new_item)
                    save_articles(articles)
                    status_msg = "Saved successfully"
                else:
                    status_msg = "Already in saved list"

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self._send_cors()
                self.end_headers()
                resp = {
                    "status": "success",
                    "message": status_msg,
                    "total_saved": len(articles),
                    "article": {"title": title, "url": url}
                }
                self.wfile.write(json.dumps(resp).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self._send_cors()
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self._send_cors()
            self.end_headers()

    def do_GET(self):
        if self.path == "/saved-articles":
            articles = load_saved()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors()
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "articles": articles}).encode("utf-8"))
        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors()
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_response(404)
            self._send_cors()
            self.end_headers()

    def log_message(self, format, *args):
        # Clean logging
        sys.stderr.write(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}\n")

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), NewsAPIHandler)
    print(f"News24 NotebookLM Backend API running on port {PORT}...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
