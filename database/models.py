from database.database import get_connection
from security.encryption import encrypt_password, decrypt_password


class User:

    @staticmethod
    def create(username, password):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(username, password) VALUES(?, ?)",
            (username, password)
        )

        conn.commit()
        conn.close()

    @staticmethod
    def exists(username):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        conn.close()

        return user is not None

    @staticmethod
    def get_by_username(username):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        conn.close()

        return user

    @staticmethod
    def set_pin(user_id, pin_hash):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE users SET pin_hash=? WHERE id=?",
            (pin_hash, user_id)
        )

        conn.commit()
        conn.close()

    @staticmethod
    def get_pin_hash(user_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT pin_hash FROM users WHERE id=?", (user_id,))
        row = cursor.fetchone()

        conn.close()

        return row[0] if row else None

    @staticmethod
    def has_pin(user_id):
        pin_hash = User.get_pin_hash(user_id)
        return pin_hash is not None and pin_hash != ""


class Password:

    @staticmethod
    def create(user_id, title, username, password, website, category):

        encrypted = encrypt_password(password)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO passwords(user_id, title, username, password, website, category)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, title, username, encrypted, website, category)
        )

        conn.commit()
        conn.close()

    @staticmethod
    def get_all(user_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM passwords WHERE user_id=? ORDER BY id DESC",
            (user_id,)
        )

        rows = cursor.fetchall()
        conn.close()

        decrypted_rows = []

        for row in rows:
            row = list(row)
            row[4] = decrypt_password(row[4])
            decrypted_rows.append(tuple(row))

        return decrypted_rows

    @staticmethod
    def delete(password_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM passwords WHERE id=?", (password_id,))

        conn.commit()
        conn.close()

    @staticmethod
    def update(password_id, title, username, password, website, category):

        encrypted = encrypt_password(password)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE passwords
            SET title=?, username=?, password=?, website=?, category=?
            WHERE id=?
            """,
            (title, username, encrypted, website, category, password_id)
        )

        conn.commit()
        conn.close()
