from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import json
import os

# FLASK
app = Flask(__name__)

app.secret_key = "VAK-SMA1-SECRET-KEY-2026"

# FOLDER
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

CSV_PATH = os.path.join(
    DATABASE_DIR,
    "SMA1_DATABASE.csv"
)

TOKEN_PATH = os.path.join(
    DATABASE_DIR,
    "token.json"
)

# KOLOM CSV
REQUIRED_COLUMNS = [
    "Inisial",
    "Kelas",
    "Rombel",
    "Sekolah",
    "Jurusan",

    "Visual",
    "Auditori",
    "Kinestetik",

    "Visual_prop",
    "Auditori_prop",
    "Kinestetik_prop",

    "KMeans_Cluster",
    "KMeans_Gaya_Belajar",

    "FCM_Membership_Cluster_0",
    "FCM_Membership_Cluster_1",
    "FCM_Membership_Cluster_2",

    "FCM_Cluster",
    "FCM_Gaya_Belajar",
    "FCM_Derajat_Keanggotaan"
]

# LOAD CSV
def load_data():

    if not os.path.exists(CSV_PATH):

        raise FileNotFoundError(
            f"File CSV tidak ditemukan:\n{CSV_PATH}"
        )

    df = pd.read_csv(
        CSV_PATH
    )

    # Bersihkan nama kolom
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace("**", "", regex=False)
    )

    # Cek kolom
    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing:

        raise ValueError(
            "Kolom CSV tidak lengkap.\n"
            f"Kolom yang hilang: {missing}"
        )

    return df

# LOAD TOKEN JSON
def load_tokens():

    if not os.path.exists(TOKEN_PATH):

        raise FileNotFoundError(
            f"File token.json tidak ditemukan:\n{TOKEN_PATH}"
        )

    with open(
        TOKEN_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    if not isinstance(data, list):

        raise ValueError(
            "token.json harus berbentuk LIST."
        )

    return data

# AUTENTIKASI USER
def authenticate_user(
    inisial,
    token,
    role
):

    users = load_tokens()

    inisial_input = str(
        inisial
    ).strip().lower()

    token_input = str(
        token
    ).strip().lower()

    role_input = str(
        role
    ).strip().lower()


    for user in users:

        if not isinstance(user, dict):
            continue

        user_inisial = str(
            user.get("Inisial", "")
        ).strip().lower()

        user_token = str(
            user.get("Token", "")
        ).strip().lower()

        user_role = str(
            user.get("Role", "")
        ).strip().lower()


        # --------------------------------------------
        # Cocokkan
        # --------------------------------------------

        if (
            user_inisial == inisial_input
            and
            user_token == token_input
            and
            user_role == role_input
        ):

            return user


    return None

# CARI SISWA DI CSV
def find_student(inisial):

    df = load_data()

    target = str(
        inisial
    ).strip().lower()

    mask = (
        df["Inisial"]
        .astype(str)
        .str.strip()
        .str.lower()
        == target
    )

    result = df.loc[mask]

    if result.empty:

        return None

    return result.iloc[0].to_dict()

# HALAMAN TENTANG PENELITIAN
@app.route("/")
def tentang_penelitian():

    return render_template(
        "tentang.html"
    )

# LOGIN
@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    # --------------------------------------------------------
    # GET
    # --------------------------------------------------------

    if request.method == "GET":

        return render_template(
            "login.html"
        )


    # --------------------------------------------------------
    # AMBIL FORM
    # --------------------------------------------------------

    role = request.form.get(
        "role",
        ""
    ).strip().lower()

    inisial = request.form.get(
        "inisial",
        ""
    ).strip()

    token = request.form.get(
        "token",
        ""
    ).strip()


    # --------------------------------------------------------
    # VALIDASI ROLE
    # --------------------------------------------------------

    if role not in ["guru", "siswa"]:

        return render_template(
            "login.html",
            error="Silakan pilih Guru atau Siswa."
        )


    # --------------------------------------------------------
    # VALIDASI INISIAL
    # --------------------------------------------------------

    if not inisial:

        return render_template(
            "login.html",
            error="Inisial harus diisi."
        )


    # --------------------------------------------------------
    # VALIDASI TOKEN
    # --------------------------------------------------------

    if not token:

        return render_template(
            "login.html",
            error="Token harus diisi."
        )


    # ========================================================
    # AUTENTIKASI
    # ========================================================

    user = authenticate_user(
        inisial,
        token,
        role
    )


    # --------------------------------------------------------
    # LOGIN GAGAL
    # --------------------------------------------------------

    if user is None:

        return render_template(
            "login.html",
            error=(
                "Inisial, token, atau jenis pengguna "
                "tidak sesuai."
            )
        )


    # ========================================================
    # GURU
    # ========================================================

    if role == "guru":

        session.clear()

        session["logged_in"] = True
        session["role"] = "guru"
        session["inisial"] = user["Inisial"]


        return redirect(
            url_for("index")
        )


    # ========================================================
    # SISWA
    # ========================================================

    if role == "siswa":

        # --------------------------------------------
        # Cari data siswa di CSV
        # --------------------------------------------

        student = find_student(
            user["Inisial"]
        )


        # --------------------------------------------
        # Token benar tetapi siswa tidak ada di CSV
        # --------------------------------------------

        if student is None:

            return render_template(
                "login.html",
                error=(
                    f"Token benar, tetapi inisial "
                    f"{user['Inisial']} tidak ditemukan "
                    "di SMA1_DATABASE.csv."
                )
            )


        # --------------------------------------------
        # Simpan session
        # --------------------------------------------

        session.clear()

        session["logged_in"] = True
        session["role"] = "siswa"
        session["inisial"] = user["Inisial"]


        # --------------------------------------------
        # LANGSUNG TAMPILKAN HASIL
        #
        # Tidak redirect ke /hasil terlebih dahulu.
        # --------------------------------------------

        return render_template(
            "hasil.html",
            data=student
        )

# INDEX GURU
@app.route("/index")
def index():

    if session.get("role") != "guru":

        return redirect(
            url_for("login")
        )


    return render_template(
        "index.html"
    )

# SEARCH GURU
@app.route("/search")
def search():

    if session.get("role") != "guru":

        return redirect(
            url_for("login")
        )


    query = request.args.get(
        "inisial",
        ""
    ).strip()


    if not query:

        return render_template(
            "index.html",
            error="Masukkan inisial terlebih dahulu."
        )


    df = load_data()


    mask = (
        df["Inisial"]
        .astype(str)
        .str.strip()
        .str.lower()
        .str.contains(
            query.lower(),
            na=False
        )
    )


    results = df.loc[
        mask,
        [
            "Inisial",
            "Sekolah",
            "Kelas",
            "Rombel"
        ]
    ].copy()


    if results.empty:

        return render_template(
            "index.html",
            error=(
                f"Tidak ditemukan peserta "
                f"dengan inisial '{query}'."
            )
        )


    results = results.to_dict(
        orient="records"
    )


    return render_template(
        "index.html",
        search_results=results,
        search_query=query
    )

# HASIL DETAIL
@app.route(
    "/hasil/<inisial>"
)
def hasil(inisial):

    # --------------------------------------------------------
    # Harus login
    # --------------------------------------------------------

    if not session.get("logged_in"):

        return redirect(
            url_for("login")
        )


    # --------------------------------------------------------
    # Siswa hanya boleh melihat dirinya sendiri
    # --------------------------------------------------------

    if session.get("role") == "siswa":

        logged_user = str(
            session.get("inisial", "")
        ).strip().lower()

        requested_user = str(
            inisial
        ).strip().lower()


        if logged_user != requested_user:

            return redirect(
                url_for(
                    "hasil",
                    inisial=session["inisial"]
                )
            )


    # --------------------------------------------------------
    # Ambil data
    # --------------------------------------------------------

    student = find_student(
        inisial
    )


    if student is None:

        return render_template(
            "index.html",
            error=(
                f"Data dengan inisial "
                f"'{inisial}' tidak ditemukan."
            )
        )


    return render_template(
        "hasil.html",
        data=student
    )

# REKOMENDASI VISUAL
@app.route(
    "/rekomendasi/visual"
)
def rekomendasi_visual():

    if not session.get("logged_in"):

        return redirect(
            url_for("login")
        )

    return render_template(
        "rekomendasi_visual.html"
    )

# REKOMENDASI AUDITORI
@app.route(
    "/rekomendasi/auditori"
)
def rekomendasi_auditori():

    if not session.get("logged_in"):

        return redirect(
            url_for("login")
        )

    return render_template(
        "rekomendasi_auditori.html"
    )

# REKOMENDASI KINESTETIK
@app.route(
    "/rekomendasi/kinestetik"
)
def rekomendasi_kinestetik():

    if not session.get("logged_in"):

        return redirect(
            url_for("login")
        )

    return render_template(
        "rekomendasi_kinestetik.html"
    )

# LOGOUT
@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("tentang_penelitian")
    )

# RUN
if __name__ == "__main__":

    app.run(
        debug=True
    )