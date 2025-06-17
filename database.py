import sqlite3

conn = sqlite3.connect("db.sqlite3")
c = conn.cursor()

def init_db():
    c.execute('''
        CREATE TABLE IF NOT EXISTS access_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reservation_id TEXT UNIQUE,
            pin_code TEXT,
            valid_from TEXT,
            valid_to TEXT,
            sent INTEGER DEFAULT 0
        )
    ''')
    conn.commit()

def pin_exists(reservation_id):
    c.execute("SELECT 1 FROM access_codes WHERE reservation_id = ?", (reservation_id,))
    return c.fetchone() is not None

def was_pin_sent(reservation_id):
    c.execute("SELECT sent FROM access_codes WHERE reservation_id = ?", (reservation_id,))
    row = c.fetchone()
    return row is not None and row[0] == 1

def store_pin(reservation_id, pin_code, valid_from, valid_to):
    try:
        c.execute(
            "INSERT INTO access_codes (reservation_id, pin_code, valid_from, valid_to) VALUES (?, ?, ?, ?)",
            (reservation_id, pin_code, valid_from, valid_to)
        )
        conn.commit()
        print(f"PIN {pin_code} uložen pro rezervaci {reservation_id}")
    except sqlite3.IntegrityError:
        print(f"PIN pro rezervaci {reservation_id} už existuje")

def get_pin(reservation_id):
    c.execute("SELECT pin_code, valid_from, valid_to FROM access_codes WHERE reservation_id = ?", (reservation_id,))
    return c.fetchone()

def mark_pin_sent(reservation_id):
    c.execute("UPDATE access_codes SET sent = 1 WHERE reservation_id = ?", (reservation_id,))
    conn.commit()

def close_db():
    c.close()
    conn.close()
