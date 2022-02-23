import sqlite3
from helper import message
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

class User:
    def __init__(self, database):
        db = database
        # db.row_factory = sqlite3.Row

        user = db.execute("SELECT * FROM users WHERE users.email = ?", [request.form.get("email")]).fetchall()[0]

        # Check if user exists
        if not user:
            return message("No such user. Try to register")

        self.__id = user['id']
        self.__last_name = user['lastName']
        self.__first_name = user['firstName']
        self.__email = user['email']
        self.__date_of_birth = user['dateOfBirth']
        self.__hash = user['hash']
    
    def check_password(self, password):
        if check_password_hash(self.__hash, password):
            return True
        else:
            return False

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
    