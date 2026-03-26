import urllib.request
import urllib.error
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer

class CORSProxyHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, x-api-key, anthropic-version')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # Hugging Face sometimes appends query parameters like /?logs=container
        if self.path == '/' or self.path.startswith('/?'):
            self.path = '/market-scout.html'
        super().do_GET()
        
    def do_POST(self):
        if self.path == '/api/anthropic':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Forward headers securely
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': self.headers.get('x-api-key', ''),
                'anthropic-version': self.headers.get('anthropic-version', '2023-06-01')
            }
            
            req = urllib.request.Request('https://api.anthropic.com/v1/messages', data=post_data, headers=headers, method='POST')
            try:
                with urllib.request.urlopen(req) as response:
                    res_body = response.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(res_body)
            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(e.read())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self.send_error(404, "Not Found")

if __name__ == '__main__':
    port = 7860
    server_address = ('', port)
    httpd = HTTPServer(server_address, CORSProxyHandler)
    print(f"🚀 Servidor Local DUAL-AI activo en: http://localhost:{port}")
    print(f"📡 Proxy API configurado en: /api/anthropic")
    print(f"Presiona Ctrl+C para detener")
    httpd.serve_forever()
