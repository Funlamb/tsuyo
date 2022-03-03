import os
# import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
import sqlite3

def message(message):
    """Render a message to the user"""
    return render_template("message.html", message=message)

def get_db_connection():
   db = sqlite3.connect("workout.db", check_same_thread=False)
   db.row_factory = sqlite3.Row
   return db