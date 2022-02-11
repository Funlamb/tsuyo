from flask import Flask, redirect, render_template, request, session

import sqlite3

app = Flask(__name__)

def get_db_connection():
   db = sqlite3.connect("workout.db")
   db.row_factory = sqlite3.Row
   return db

@app.route('/')
def index():
   db = get_db_connection()
   posts = db.execute("SELECT * FROM users").fetchall()
   db.close()
   return render_template("index.html", posts=posts)

if __name__ == '__main__':
   app.run()