import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

class User:
    def __init__(self, database, email):
        db = database

        user = db.execute("SELECT * FROM users WHERE users.email = ?", [email]).fetchall()[0]

        self.__id = user['id']
        self.__last_name = user['lastName']
        self.__first_name = user['firstName']
        self.__email = user['email']
        self.__date_of_birth = user['dateOfBirth']
        self.__hash = user['hash']
    
    def check_password(self, password):
        print(self.__hash)
        print(generate_password_hash(password))
        if check_password_hash(self.__hash, password):
            return True
        else:
            return False

    def change_user_data(self, db, ls):
        print(generate_password_hash (ls['original_password']))
        print(self.__hash)
        if not check_password_hash(self.__hash, ls['original_password']):
            return 1

        # Change last name
        if ls['last_name']:
            temp = [ls['last_name'], self.__id]
            db.execute("UPDATE users SET lastName = ? WHERE id = ?", temp)
      
        # Change first name
        if ls['first_name']:
            temp = [ls['first_name'], self.__id]
            db.execute("UPDATE users SET firstName = ? WHERE id = ?", temp)
        
        if ls['email']:
            temp = [ls['email'], self.__id]
            db.execute("UPDATE users SET email = ? WHERE id = ?", temp)

        if ls['date_of_birth']:
            temp = [ls['date_of_birth'], self.__id]
            db.execute("UPDATE users SET dateOfBirth = ? WHERE id = ?", temp)
        
        # # Change password
        if ls['change_password'] or ls['confirm_password']:
            if ls['change_password'] != ls['confirm_password']:
                return 2 # Change_password and Confirm_password do not match
            temp = [generate_password_hash(ls['change_password']), self.__id]
            db.execute("UPDATE users SET hash = ? WHERE id = ?", temp)
        
        db.commit()
        return 0 # Worked

    def get_id(self):
        return self.__id
    
    def get_last_name(self):
        return self.__last_name
    
    def get_first_name(self):
        return self.__first_name
    
    def get_email(self):
        return self.__email
        
    def get_date_of_birth(self):
        return self.__date_of_birth
    