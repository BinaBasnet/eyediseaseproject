from models.database import Database
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, name, email, password, role='user'):
        self.name = name
        self.email = email
        # Hash the password
        self.password = generate_password_hash(password)
        # Role can be 'user' or 'admin'
        self.role = role

    # Save user/admin to database
    def save(self):
        db = Database()
        query = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"
        db.cursor.execute(query, (self.name, self.email, self.password, self.role))
        db.commit()
        db.close()

    # Get user/admin by email
    @staticmethod
    def get_by_email(email):
        db = Database()
        query = "SELECT * FROM users WHERE email=%s"
        db.cursor.execute(query, (email,))
        user = db.cursor.fetchone()
        db.close()
        return user

    # Verify password for login
    @staticmethod
    def verify_password(email, password):
        user = User.get_by_email(email)
        if user and check_password_hash(user['password'], password):
            return user
        return None