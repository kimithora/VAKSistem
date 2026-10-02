
import os
import mysql.connector


def get_db_connection():

    # ========================================================
    # CEK APAKAH APLIKASI BERJALAN DI VERCEL
    # ========================================================

    is_vercel = os.environ.get("VERCEL") == "1"

    # ========================================================
    # KONFIGURASI DATABASE LOKAL
    # ========================================================

    if not is_vercel:

        return mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="",
            database="vak_sistem"
        )

    # ========================================================
    # KONFIGURASI DATABASE VERCEL
    # ========================================================

    db_host = os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT", "3306")
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_name = os.environ.get("DB_NAME")

    # ========================================================
    # CEK ENVIRONMENT VARIABLE VERCEL
    # ========================================================

    missing = []

    if not db_host:
        missing.append("DB_HOST")

    if not db_user:
        missing.append("DB_USER")

    if not db_name:
        missing.append("DB_NAME")

    if missing:

        raise RuntimeError(
            "Environment variable database belum lengkap: "
            + ", ".join(missing)
        )

    # ========================================================
    # KONEKSI DATABASE VERCEL
    # ========================================================

    return mysql.connector.connect(
        host=db_host,
        port=int(db_port),
        user=db_user,
        password=db_password or "",
        database=db_name,
        ssl_disabled=False
    )


# ============================================================
# TEST DATABASE CONNECTION
# ============================================================

if __name__ == "__main__":

    try:

        db = get_db_connection()

        print("=" * 50)
        print("Koneksi database berhasil!")
        print("=" * 50)

        db.close()

    except Exception as e:

        print("=" * 50)
        print("Koneksi database gagal!")
        print("Error:", e)
        print("=" * 50)