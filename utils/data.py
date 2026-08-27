import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "SMA1_DATABASE.csv"


def load_students():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"File database tidak ditemukan: {DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE)

    df.columns = df.columns.str.strip()

    return df


def get_student_by_initial(inisial):
    df = load_students()

    hasil = df[
        df["Inisial"].astype(str).str.strip().str.lower()
        == str(inisial).strip().lower()
    ]

    if hasil.empty:
        return None

    return hasil.iloc[0].to_dict()


def search_students(keyword):
    df = load_students()

    keyword = str(keyword).strip().lower()

    if not keyword:
        return []

    hasil = df[
        df["Inisial"].astype(str)
        .str.strip()
        .str.lower()
        .str.contains(keyword, na=False)
    ]

    return hasil.to_dict(orient="records")