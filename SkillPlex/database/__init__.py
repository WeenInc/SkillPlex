import sqlite3

def initialize_db(db_url):
    conn = sqlite3.connect(db_url)
    cur = conn.cursor()
    
    # Create the conversations table with conversation_id as TEXT
    cur.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY,
            conversation_id TEXT NOT NULL
        )
    ''')

    # Create the messages table with conversation_id as TEXT and foreign key relationship
    cur.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            conversation_id TEXT,
            message TEXT,
            FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id)
        )
    ''')
    
    conn.commit()
    conn.close()