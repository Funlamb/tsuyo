import os

from flask import redirect, render_template, request, session
from functools import wraps
import sqlite3

def message(message, title):
    """Render a message to the user"""
    return render_template("message.html", message=message, name=title)

def get_db_connection():
   db = sqlite3.connect("workout.db", check_same_thread=False)
   db.row_factory = sqlite3.Row
   return db

def default(obj):
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function