import sqlite3
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

def get_latest_team_data(db_path="pfsense_session_IDs.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    latest_data = []
    
    for i in range(1, 16):
        # Maps to your "Team X" format
        table_name = f"Team {i}" 
        try:
            # Matches your exact table and column names
            query = f"""
                SELECT pfsense_address, client_address, session_id, browser, timestamp 
                FROM '{table_name}' 
                ORDER BY timestamp DESC 
                LIMIT 1
            """
            cursor.execute(query)
            row = cursor.fetchone()
            
            if row:
                latest_data.append({
                    "team": table_name,
                    "pfsense_ip": "http://" + row[0],   # Maps pfsense_address to the HTML
                    "client_ip": row[1],    # Maps client_address to the HTML
                    "session_id": row[2],
                    "browser": row[3],
                    "timestamp": row[4]
                })
            else:
                latest_data.append({"team": table_name, "status": "No data"})
                
        except sqlite3.OperationalError:
            # Fails gracefully if your script hasn't created this team's table yet
            latest_data.append({"team": table_name, "status": "No data"})

    conn.close()
    return latest_data

class MonitorHandler(BaseHTTPRequestHandler):
    # Suppress default HTTP logging to keep your terminal clean
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == '/api/latest':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = get_latest_team_data()
            self.wfile.write(json.dumps(data).encode('utf-8'))
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            try:
                with open('index.html', 'rb') as f:
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.wfile.write(b"index.html not found in the current directory.")

def start_server():
    port = 8080
    server = HTTPServer(('0.0.0.0', port), MonitorHandler)
    print(f"[*] Monitor server running on http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down monitor server.")
        server.server_close()

if __name__ == "__main__":
    start_server()
