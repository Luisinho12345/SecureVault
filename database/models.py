from database.database import get_connection


class User:

    @staticmethod
    def create(username, password):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users(username, password)
            VALUES(?, ?)
            """,
            (username, password)
        )

        conn.commit()
        conn.close()

    @staticmethod
    def exists(username):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE username=?",
            (username,)
        )

        user = cursor.fetchone()

        conn.close()

        return user is not None