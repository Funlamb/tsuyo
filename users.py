import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
# from . import workout.db # This line breaks my code

class User:
    db = None

    def __init__(self, id, last_name, first_name, email, date_of_birth, hash):
        self.id = id
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
        self.date_of_birth = date_of_birth
        self.hash = hash

    @staticmethod
    def get(email):
        user_result = User.db.execute("SELECT * FROM users WHERE users.email LIKE ?", [email]).fetchone()
        if user_result:
            return User(user_result[0], user_result[1], user_result[2], user_result[3], user_result[4], user_result[5])
        else: 
            return None

    def check_password(self, password):
        if check_password_hash(self.hash, password):
            return True
        else:
            return False
    
    @staticmethod
    def add_user(ls):
        User.db.execute("INSERT INTO users (lastName, firstName, email, dateOfBirth, hash) VALUES (?, ?, ?, ?, ?)", ls)
        User.db.commit() # Need to commit the changes or it will not save to the database
    
    def change_user_data(self, ls):
        if not check_password_hash(self.hash, ls['original_password']):
            return 1 # Original password does not match

        # Change last name
        if ls['last_name']:
            temp = [ls['last_name'], self.id]
            User.db.execute("UPDATE users SET lastName = ? WHERE id = ?", temp)
      
        # Change first name
        if ls['first_name']:
            temp = [ls['first_name'], self.id]
            User.db.execute("UPDATE users SET firstName = ? WHERE id = ?", temp)
        
        if ls['email']:
            temp = [ls['email'], self.id]
            User.db.execute("UPDATE users SET email = ? WHERE id = ?", temp)

        if ls['date_of_birth']:
            temp = [ls['date_of_birth'], self.id]
            User.db.execute("UPDATE users SET dateOfBirth = ? WHERE id = ?", temp)
        
        # # Change password
        if ls['change_password'] or ls['confirm_password']:
            if ls['change_password'] != ls['confirm_password']:
                return 2 # Change_password and Confirm_password do not match
            temp = [generate_password_hash(ls['change_password']), self.id]
            User.db.execute("UPDATE users SET hash = ? WHERE id = ?", temp)
        
        User.db.commit()
        return 0 # Worked

    def get_id(self):
        return self.id
    
    def get_last_name(self):
        return self.last_name
    
    def get_first_name(self):
        return self.first_name
    
    def get_email(self):
        return self.email
        
    def get_date_of_birth(self):
        return self.date_of_birth
    