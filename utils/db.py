import os
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        ssl_disabled=False
    )


if __name__ == "__main__":
    db = get_db_connection()
    print("Koneksi database berhasil!")
    db.close()