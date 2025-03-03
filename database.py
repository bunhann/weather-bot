import sqlite3

def initialize_db():
    conn = sqlite3.connect('./db/weather_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            gender TEXT,
            age_group TEXT,
            latitude REAL,
            longitude REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_user_info(user_id, gender, age_group):
    conn = sqlite3.connect('./db/weather_bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO users (user_id, gender, age_group) VALUES (?, ?, ?)', (user_id, gender, age_group))
    conn.commit()
    conn.close()

def save_location(user_id, latitude, longitude):
    conn = sqlite3.connect('./db/weather_bot.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET latitude = ?, longitude = ? WHERE user_id = ?', (latitude, longitude, user_id))
    conn.commit()
    conn.close()