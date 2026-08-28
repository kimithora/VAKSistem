from flask import Flask, render_template, request, redirect, url_for, session
from pathlib import Path

from utils.data import (
    search_students,
    get_student_by_initial,
    get_dashboard_statistics
)

from utils.auth import authenticate


# =========================================================
# PATH PROJECT
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

TEMPLATES_DIR = BASE_DIR / "template"
STATIC_DIR = BASE_DIR / "static"


# =========================================================
# FLASK APP
# =========================================================

app = Flask(
    __name__,
    template_folder=str(TEMPLATES_DIR),
    static_folder=str(STATIC_DIR)
)

app.secret_key = "vak-research-development-key"


# =========================================================
# CEK PROJECT
# =========================================================

print("=" * 60)
print("PROJECT PATH    :", BASE_DIR)
print("TEMPLATE PATH   :", TEMPLATES_DIR)
print("STATIC PATH     :", STATIC_DIR)
print("TEMPLATE EXISTS :", TEMPLATES_DIR.exists())
print("STATIC EXISTS   :", STATIC_DIR.exists())
print(
    "TENTANG EXISTS  :",
    (TEMPLATES_DIR / "tentang.html").exists()
)
print(
    "LOGIN EXISTS    :",
    (TEMPLATES_DIR / "login.html").exists()
)
print(
    "CSV EXISTS      :",
    (BASE_DIR / "SMA1_DATABASE.csv").exists()
)
print(
    "TOKEN EXISTS    :",
    (BASE_DIR / "token.json").exists()
)
print("=" * 60)


# =========================================================
# TENTANG PENELITIAN
# =========================================================

@app.route("/")
def tentang():

    return render_template("tentang.html")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        token = request.form.get("token", "").strip()

        # ---------------------------------------------
        # TOKEN KOSONG
        # ---------------------------------------------

        if not token:

            error = "Silakan masukkan token."

            return render_template(
                "login.html",
                error=error
            )


        # ---------------------------------------------
        # AUTENTIKASI
        # ---------------------------------------------

        user = authenticate(token)

        if user is None:

            error = "Token tidak valid."

            return render_template(
                "login.html",
                error=error
            )


        # ---------------------------------------------
        # SIMPAN SESSION
        # ---------------------------------------------

        session.clear()

        session["logged_in"] = True
        session["inisial"] = user["Inisial"]
        session["token"] = user["Token"]
        session["role"] = user["Role"]


        # ---------------------------------------------
        # REDIRECT BERDASARKAN ROLE
        # ---------------------------------------------

        role = user["Role"].lower()

        if role == "guru":

            return redirect(
                url_for("dashboard_guru")
            )

        elif role == "siswa":

            return redirect(
                url_for("hasil_siswa")
            )


        # ---------------------------------------------
        # ROLE TIDAK DIKENALI
        # ---------------------------------------------

        session.clear()

        error = "Role pengguna tidak dikenali."

    return render_template(
        "login.html",
        error=error
    )


# =========================================================
# DASHBOARD GURU
# =========================================================

@app.route("/guru")
def dashboard_guru():

    # ---------------------------------------------
    # CEK LOGIN
    # ---------------------------------------------

    if not session.get("logged_in"):

        return redirect(
            url_for("login")
        )


    # ---------------------------------------------
    # CEK ROLE
    # ---------------------------------------------

    if session.get("role", "").lower() != "guru":

        return redirect(
            url_for("login")
        )


    # ---------------------------------------------
    # SEARCH SISWA
    # ---------------------------------------------

    keyword = request.args.get(
        "search",
        ""
    ).strip()

    students = []

    if keyword:

        students = search_students(
            keyword
        )


    # ---------------------------------------------
    # STATISTIK DATABASE
    # ---------------------------------------------

    statistics = get_dashboard_statistics()


    # ---------------------------------------------
    # RENDER DASHBOARD
    # ---------------------------------------------

    return render_template(
        "guru/dashboard.html",
        students=students,
        keyword=keyword,
        statistics=statistics
    )


# =========================================================
# HASIL SISWA - AKSES GURU
# =========================================================

@app.route("/guru/siswa/<inisial>")
def hasil_siswa_guru(inisial):

    # ---------------------------------------------
    # CEK LOGIN
    # ---------------------------------------------

    if not session.get("logged_in"):

        return redirect(
            url_for("login")
        )


    # ---------------------------------------------
    # CEK ROLE GURU
    # ---------------------------------------------

    if session.get("role", "").lower() != "guru":

        return redirect(
            url_for("login")
        )


    # ---------------------------------------------
    # AMBIL DATA SISWA
    # ---------------------------------------------

    student = get_student_by_initial(
        inisial
    )


    if student is None:

        return (
            "Data siswa tidak ditemukan.",
            404
        )


    # ---------------------------------------------
    # TAMPILKAN HASIL
    # ---------------------------------------------

    return render_template(
        "guru/hasil_siswa.html",
        student=student
    )


# =========================================================
# HASIL SISWA - AKSES SISWA
# =========================================================

@app.route("/siswa")
def hasil_siswa():

    # ---------------------------------------------
    # CEK LOGIN
    # ---------------------------------------------

    if not session.get("logged_in"):

        return redirect(
            url_for("login")
        )


    # ---------------------------------------------
    # CEK ROLE SISWA
    # ---------------------------------------------

    if session.get("role", "").lower() != "siswa":

        return redirect(
            url_for("login")
        )


    # ---------------------------------------------
    # AMBIL INISIAL DARI SESSION
    # ---------------------------------------------

    inisial = session.get(
        "inisial"
    )


    # ---------------------------------------------
    # AMBIL DATA SISWA
    # ---------------------------------------------

    student = get_student_by_initial(
        inisial
    )


    if student is None:

        session.clear()

        return (
            "Data siswa tidak ditemukan.",
            404
        )


    # ---------------------------------------------
    # TAMPILKAN HASIL
    # ---------------------------------------------

    return render_template(
        "siswa/hasil.html",
        student=student
    )


# =========================================================
# REKOMENDASI VISUAL
# =========================================================

@app.route("/rekomendasi/visual")
def rekomendasi_visual():

    if not session.get("logged_in"):

        return redirect(
            url_for("login")
        )

    return render_template(
        "rekomendasi/rekomendasi_visual.html"
    )


# =========================================================
# REKOMENDASI AUDITORI
# =========================================================

@app.route("/rekomendasi/auditori")
def rekomendasi_auditori():

    if not session.get("logged_in"):

        return redirect(
            url_for("login")
        )

    return render_template(
        "rekomendasi/rekomendasi_auditori.html"
    )


# =========================================================
# REKOMENDASI KINESTETIK
# =========================================================

@app.route("/rekomendasi/kinestetik")
def rekomendasi_kinestetik():

    if not session.get("logged_in"):

        return redirect(
            url_for("login")
        )

    return render_template(
        "rekomendasi/rekomendasi_kinestetik.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("tentang")
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
