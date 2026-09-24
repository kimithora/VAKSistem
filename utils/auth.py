from utils.db import get_db_connection


def authenticate(token):
    token = str(token).strip()

    if not token:
        return None

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT Token, Inisial, Role
        FROM akun_pengguna
        WHERE Token = %s
    """

    cursor.execute(query, (token,))
    user = cursor.fetchone()

    cursor.close()
    db.close()

    return user


def get_user_by_initial(inisial):

    inisial = str(inisial).strip()

    if not inisial:
        return None

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT Token, Inisial, Role
        FROM akun_pengguna
        WHERE LOWER(Inisial) = LOWER(%s)
        LIMIT 1
    """

    cursor.execute(query, (inisial,))
    user = cursor.fetchone()

    cursor.close()
    db.close()

    return user