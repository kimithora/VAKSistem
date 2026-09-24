import mysql.connector


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="vak_sistem"
    )


if __name__ == "__main__":
    db = get_db_connection()
    print("Koneksi database berhasil!")
    db.close()