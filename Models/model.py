from werkzeug.security import generate_password_hash
from Config import db

class User():

    @staticmethod
    def getall(db):
        cur = db.execute('select * from users')
        users = cur.fetchall()
        return users

    @staticmethod
    def add_new(db, name, email, password):
        db.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
        (name, email, generate_password_hash(password)))
        db.commit()

    @staticmethod
    def check(db, username):
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        return user

    @staticmethod
    def display_one(db, userid):
        user = db.execute(
            'SELECT * FROM users WHERE id = ?', (userid,)
        ).fetchone()
        return user

    @staticmethod
    def delete_user(db, id):
        db.execute(
            'DELETE FROM users WHERE id = ?', (id,)
        )
        db.commit()

    @staticmethod
    def update_user(db, id, name, email, password):
        db.execute(
            'UPDATE users SET username = ?, email = ?, password = ? WHERE id = ?', 
            (name, email, generate_password_hash(password), id)
        )
        db.commit()
