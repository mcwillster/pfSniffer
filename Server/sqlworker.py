import sqlite3
import time
import random

DATABASE_FILEPATH = "pfsense_session_IDs.db"

#Function to insert an entry in my pfsense master database
def insert(client_ip, pfsense_ip, session_id, browser, logged_in):

    #setup: connect to database, then make cursor, and split apart pfsense_ip to get table_name
    connection = sqlite3.connect(DATABASE_FILEPATH)
    cursor = connection.cursor()
    
    ip_lst = pfsense_ip.split('.')
    table_name = "Team " + ip_lst[1]

    #sqlite cursor doing my bidding, making the table for the team this entry originates from
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS "{table_name}" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_address VARCHAR(15) NOT NULL,
            pfsense_address VARCHAR(15) NOT NULL,
            session_id TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            browser TEXT NOT NULL,
            logged_in BOOLEAN NOT NULL DEFAULT 0 CHECK (logged_in IN (0, 1))
        )
    """)

    #sqlite cursor doing my bidding once again like a good minion, insert entry
    cursor.execute(
        f"INSERT INTO '{table_name}' (client_address, pfsense_address, session_id, browser, logged_in) values(?, ?, ?, ?, ?)", 
        (client_ip, pfsense_ip, session_id, browser, logged_in)
    )
    #git workflow fire 
    connection.commit()
    connection.close()

#main function just so I can quickly and easily test changes I make to the database
def main():
    i=1
    while i<21:
        temp_clip = f"10.{i}.1.10"
        temp_pfip = f"10.{i}.1.254"
        temp_id = f"Test{i}"
        temp_browser = "Firefox"
        logged_in = random.randint(0,1)
        insert(temp_clip, temp_pfip, temp_id, temp_browser, logged_in)
        i += 1
        time.sleep(.5)

if __name__ == "__main__":
    main()