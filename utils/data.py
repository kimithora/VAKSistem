from pathlib import Path
import pandas as pd


# =========================================================
# PATH PROJECT
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "data" / "SMA1_DATABASE.CSV"


# =========================================================
# LOAD DATABASE
# =========================================================

def load_database():

    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database tidak ditemukan.\n"
            f"Lokasi yang dicari: {DATABASE_PATH}"
        )

    return pd.read_csv(DATABASE_PATH)


# =========================================================
# SEARCH STUDENTS
# =========================================================

def search_students(keyword):

    df = load_database()

    keyword = str(keyword).strip().lower()

    if not keyword:
        return []

    mask = (
        df["Inisial"]
        .astype(str)
        .str.lower()
        .str.contains(keyword, na=False)
    )

    result = df[mask]

    return result.to_dict(orient="records")


# =========================================================
# GET STUDENT BY INITIAL
# =========================================================

def get_student_by_initial(inisial):

    df = load_database()

    inisial = str(inisial).strip().lower()

    result = df[
        df["Inisial"]
        .astype(str)
        .str.lower()
        == inisial
    ]

    if result.empty:
        return None

    return result.iloc[0].to_dict()


# =========================================================
# DASHBOARD STATISTICS
# =========================================================

def get_dashboard_statistics():

    df = load_database()

    # =====================================================
    # TOTAL SISWA
    # =====================================================

    total_siswa = len(df)

    # =====================================================
    # INFORMASI DATA
    # =====================================================

    total_kelas = (
        df["Kelas"].dropna().nunique()
        if "Kelas" in df.columns
        else 0
    )

    total_rombel = (
        df["Rombel"].dropna().nunique()
        if "Rombel" in df.columns
        else 0
    )

    total_sekolah = (
        df["Sekolah"].dropna().nunique()
        if "Sekolah" in df.columns
        else 0
    )

    total_jurusan = (
        df["Jurusan"].dropna().nunique()
        if "Jurusan" in df.columns
        else 0
    )

    # =====================================================
    # GAYA BELAJAR
    # =====================================================

    visual = 0
    auditori = 0
    kinestetik = 0

    if "KMeans_Gaya_Belajar" in df.columns:

        gaya = (
            df["KMeans_Gaya_Belajar"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        visual = int((gaya == "visual").sum())
        auditori = int((gaya == "auditori").sum())
        kinestetik = int((gaya == "kinestetik").sum())

    # =====================================================
    # RETURN STATISTICS
    # =====================================================

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