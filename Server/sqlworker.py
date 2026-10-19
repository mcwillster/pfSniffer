import sqlite3

DATABASE_FILEPATH = "pfsense_session_IDs.db"

#Function to insert an entry in my pfsense master database
def insert(client_ip, pfsense_ip, session_id, browser):

    #setup: connect to database, then make cursor, and split apart pfsense_ip to get table_name
    connection = sqlite3.connect(DATABASE_FILEPATH)
    cursor = connection.cursor()
    
    ip_lst = pfsense_ip.split('.')
    table_name = "Team " + ip_lst[2]

    #sqlite cursor doing my bidding, making the table for the team this entry originates from
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS '{table_name}' (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_address VARCHAR(15) NOT NULL,
            pfsense_address VARCHAR(15) NOT NULL,
            session_id TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            browser TEXT NOT NULL
        )
    """)

    #sqlite cursor doing my bidding once again like a good minion, insert entry
    cursor.execute(
        f"INSERT INTO '{table_name}' (client_address, pfsense_address, session_id, browser) values(?, ?, ?, ?)", 
        (client_ip, pfsense_ip, session_id, browser)
    )
    #git workflow fire 
    connection.commit()

#main function just so I can quickly and easily test changes I make to the database
def main():
    insert("192.168.1.10", "192.168.1.254", "Test1")
    insert("192.168.2.10", "192.168.2.254", "Test2")
    insert("192.168.3.11", "192.168.3.254", "Test3")

if __name__ == "__main__":
    main()