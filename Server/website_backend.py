import sqlite3
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

def get_latest_team_data(db_path="sessions.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    latest_data = []
    # Assuming your tables are named team1, team2, ... team15
    for i in range(1, 16):
        table_name = f"team{i}"
        try:
            # Fetch the most recent entry for the team
            query = f"""
                SELECT pfsense_ip, client_ip, session_id, browser, timestamp 
                FROM {table_name} 
                ORDER BY timestamp DESC 
                LIMIT 1
            """
            cursor.execute(query)
            row = cursor.fetchone()
            
            if row:
                latest_data.append({
                    "team": f"Team {i}",
                    "pfsense_ip": row[0],
                    "client_ip": row[1],
                    "session_id": row[2],
                    "browser": row[3],
                    "timestamp": row[4]
                })
            else:
                # Handle teams with no entries yet
                latest_data.append({"team": f"Team {i}", "status": "No data"})
                
        except sqlite3.OperationalError:
            pass # Table might not exist yet

    conn.close()
    return latest_data

# Example handler integration
class MonitorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/latest':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*') # In case HTML is hosted separately
            self.end_headers()
            
            data = get_latest_team_data()
            self.wfile.write(json.dumps(data).encode('utf-8'))
        elif self.path == '/':
            # Serve the HTML page below
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())