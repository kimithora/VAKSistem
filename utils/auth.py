import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
TOKEN_FILE = BASE_DIR / "data" / "token.json"


def load_tokens():
    if not TOKEN_FILE.exists():
        raise FileNotFoundError(
            f"File token tidak ditemukan: {TOKEN_FILE}"
        )

    with open(TOKEN_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(
            "Format token.json harus berupa list."
        )

    return data


def authenticate(token):
    """
    Memvalidasi token pengguna.

    Mengembalikan data pengguna jika token valid.
    Mengembalikan None jika token tidak ditemukan.
    """
    token = str(token).strip()

    if not token:
        return None

    users = load_tokens()

    for user in users:
        user_token = str(user.get("Token", "")).strip()

        if user_token == token:
            return {
                "Inisial": user.get("Inisial"),
                "Token": user.get("Token"),
                "Role": user.get("Role")
            }

    return None


def get_user_by_initial(inisial):

    inisial = str(inisial).strip().lower()

    if not inisial:
        return None

    users = load_tokens()

    for user in users:
        user_initial = str(user.get("Inisial", "")).strip().lower()

        if user_initial == inisial:
            return {
                "Inisial": user.get("Inisial"),
                "Token": user.get("Token"),
                "Role": user.get("Role")
            }

    return None