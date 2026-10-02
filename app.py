from flask import Flask, render_template, request, redirect, url_for, session
from pathlib import Path
import os

from utils.data import (
    search_students,
    get_student_by_initial,
    get_dashboard_statistics
)

from utils.auth import authenticate


# ============================================================
# PROJECT DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

TEMPLATES_DIR = BASE_DIR / "template"
STATIC_DIR = BASE_DIR / "static"
DATA_DIR = BASE_DIR / "data"

CSV_PATH = DATA_DIR / "SMA1_DATABASE.CSV"
TOKEN_PATH = DATA_DIR / "token.json"


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(
    __name__,
    template_folder=str(TEMPLATES_DIR),
    static_folder=str(STATIC_DIR)
)


# ============================================================
# SECRET KEY & SESSION
# ============================================================

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "vak-research-development-key"
)

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# HTTPS hanya digunakan ketika aplikasi berjalan di Vercel
if os.environ.get("VERCEL"):
    app.config["SESSION_COOKIE_SECURE"] = True


# ============================================================
# PROJECT CHECK
# ============================================================

print("=" * 60)
print("VAK SYSTEM - PROJECT CHECK")
print("=" * 60)

print("PROJECT PATH    :", BASE_DIR)

print("TEMPLATE PATH   :", TEMPLATES_DIR)
print("TEMPLATE EXISTS :", TEMPLATES_DIR.exists())

print("STATIC PATH     :", STATIC_DIR)
print("STATIC EXISTS   :", STATIC_DIR.exists())

print("DATA PATH       :", DATA_DIR)
print("DATA EXISTS     :", DATA_DIR.exists())

print("CSV PATH        :", CSV_PATH)
print("CSV EXISTS      :", CSV_PATH.exists())

print("TOKEN PATH      :", TOKEN_PATH)
print("TOKEN EXISTS    :", TOKEN_PATH.exists())

print(
    "TENTANG EXISTS  :",
    (TEMPLATES_DIR / "tentang.html").exists()
)

print(
    "LOGIN EXISTS    :",
    (TEMPLATES_DIR / "login.html").exists()
)

print(
    "GURU EXISTS     :",
    (TEMPLATES_DIR / "guru" / "dashboard.html").exists()
)

print(
    "HASIL GURU      :",
    (TEMPLATES_DIR / "guru" / "hasil_siswa.html").exists()
)

print(
    "HASIL SISWA     :",
    (TEMPLATES_DIR / "siswa" / "hasil.html").exists()
)

print("=" * 60)


# ============================================================
# HALAMAN UTAMA
# ============================================================

@app.route("/")
def tentang():

    return render_template(
        "tentang.html"
    )


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":

        return render_template(
            "login.html",
            error=None
        )

    token = request.form.get(
        "token",
        ""
    ).strip()

    if not token:

        return render_template(
            "login.html",
            error="Silakan masukkan token."
        )

    user = authenticate(token)

    if user is None:

        return render_template(
            "login.html",
            error="Token tidak valid."
        )

    inisial = user.get("Inisial")
    role = user.get("Role")

    if not inisial or not role:

        return render_template(
            "login.html",
            error="Data pengguna tidak lengkap."
        )

    inisial = str(inisial).strip()
    role = str(role).strip().lower()

    if role not in ("guru", "siswa"):

        return render_template(
            "login.html",
            error="Role pengguna tidak dikenali."
        )

    # Bersihkan session lama
    session.clear()

    session["logged_in"] = True
    session["inisial"] = inisial
    session["role"] = role

    # Redirect berdasarkan role
    if role == "guru":

        return redirect(
            url_for("dashboard_guru")
        )

    if role == "siswa":

        return redirect(
            url_for("hasil_siswa")
        )

    # Fallback jika terjadi kondisi yang tidak terduga
    session.clear()

    return render_template(
        "login.html",
        error="Terjadi kesalahan pada autentikasi."
    )


# ============================================================
# DASHBOARD GURU
# ============================================================

@app.route("/guru")
def dashboard_guru():

    if not session.get("logged_in"):

        return redirect(
            url_for("login")
        )

    if session.get("role", "").lower() != "guru":

        return redirect(
            url_for("login")
        )

    keyword = request.args.get(
        "search",
        ""
    ).strip()

    students = []

    if keyword:

        students = search_students(
            keyword
        )

    statistics = get_dashboard_statistics()

    return render_template(
        "guru/dashboard.html",
        students=students,
        keyword=keyword,
        statistics=statistics
    )


# ============================================================
# HASIL SISWA - DILIHAT GURU
# ============================================================

@app.route("/guru/siswa/<inisial>")
def hasil_siswa_guru(inisial):

    if not session.get("logged_in"):

        return redirect(
            url_for("login")
        )

    if session.get("role", "").lower() != "guru":

        return redirect(
            url_for("login")
        )

    inisial = str(inisial).strip()

    if not inisial:

        return (
            "Inisial siswa tidak valid.",
            400
        )

    student = get_student_by_initial(
        inisial
    )

    if student is None:

        return (
            "Data siswa tidak ditemukan.",
            404
        )

    return render_template(
        "guru/hasil_siswa.html",
        student=student
    )


# ============================================================
# HASIL SISWA
# ============================================================

@app.route("/siswa")
def hasil_siswa():

    if not session.get("logged_in"):

        return redirect(
            url_for("login")
        )

    if session.get("role", "").lower() != "siswa":

        return redirect(
            url_for("login")
        )

    inisial = session.get(
        "inisial"
    )

    if not inisial:

        session.clear()

        return redirect(
            url_for("login")
        )

    student = get_student_by_initial(
        inisial
    )

    if student is None:

        session.clear()

        return (
            "Data siswa tidak ditemukan.",
            404
        )

    return render_template(
        "siswa/hasil.html",
        student=student
    )


# ============================================================
# REKOMENDASI VISUAL
# ============================================================

@app.route("/rekomendasi/visual")
def rekomendasi_visual():

    if not session.get("logged_in"):

        return redirect(
            url_for("login")
        )

    return render_template(
        "rekomendasi/rekomendasi_visual.html"
    )


# ============================================================
# REKOMENDASI AUDITORI
# ============================================================

@app.route("/rekomendasi/auditori")
def rekomendasi_auditori():

    if not session.get("logged_in"):

        return redirect(
            url_for("login")
        )

    return render_template(
        "rekomendasi/rekomendasi_auditori.html"
    )


# ============================================================
# REKOMENDASI KINESTETIK
# ============================================================

@app.route("/rekomendasi/kinestetik")
def rekomendasi_kinestetik():

    if not session.get("logged_in"):

        return redirect(
            url_for("login")
        )

    return render_template(
        "rekomendasi/rekomendasi_kinestetik.html"
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("tentang")
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )