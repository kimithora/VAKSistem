from utils.db import get_db_connection


# =========================================================
# SEARCH STUDENTS
# =========================================================

def search_students(keyword):

    keyword = str(keyword).strip()

    if not keyword:
        return []

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    query = "SELECT * FROM siswa WHERE LOWER(Inisial) LIKE LOWER(%s)"

    cursor.execute(query, (f"%{keyword}%",))

    students = cursor.fetchall()

    cursor.close()
    db.close()

    return students


# =========================================================
# GET STUDENT BY INITIAL
# =========================================================

def get_student_by_initial(inisial):

    inisial = str(inisial).strip()

    if not inisial:
        return None

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    query = "SELECT * FROM siswa WHERE LOWER(Inisial) = LOWER(%s) LIMIT 1"

    cursor.execute(query, (inisial,))

    student = cursor.fetchone()

    cursor.close()
    db.close()

    return student


# =========================================================
# DASHBOARD STATISTICS
# =========================================================

def get_dashboard_statistics():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Total siswa
    cursor.execute("SELECT COUNT(*) AS total FROM siswa")
    total_siswa = cursor.fetchone()["total"]

    # Total kelas
    cursor.execute("SELECT COUNT(DISTINCT Kelas) AS total FROM siswa")
    total_kelas = cursor.fetchone()["total"]

    # Total rombel
    cursor.execute("SELECT COUNT(DISTINCT Rombel) AS total FROM siswa")
    total_rombel = cursor.fetchone()["total"]

    # Total sekolah
    cursor.execute("SELECT COUNT(DISTINCT Sekolah) AS total FROM siswa")
    total_sekolah = cursor.fetchone()["total"]

    # Total jurusan
    cursor.execute("SELECT COUNT(DISTINCT Jurusan) AS total FROM siswa")
    total_jurusan = cursor.fetchone()["total"]

    # Gaya belajar
    cursor.execute(
        "SELECT KMeans_Gaya_Belajar, COUNT(*) AS jumlah "
        "FROM siswa GROUP BY KMeans_Gaya_Belajar"
    )

    gaya_data = cursor.fetchall()

    visual = 0
    auditori = 0
    kinestetik = 0

    for row in gaya_data:

        gaya = str(row["KMeans_Gaya_Belajar"]).strip().lower()
        jumlah = int(row["jumlah"])

        if gaya == "visual":
            visual = jumlah

        elif gaya == "auditori":
            auditori = jumlah

        elif gaya == "kinestetik":
            kinestetik = jumlah

    cursor.close()
    db.close()

    return {
        "total_siswa": int(total_siswa),
        "total_kelas": int(total_kelas),
        "total_rombel": int(total_rombel),
        "total_sekolah": int(total_sekolah),
        "total_jurusan": int(total_jurusan),
        "visual": int(visual),
        "auditori": int(auditori),
        "kinestetik": int(kinestetik)
    }