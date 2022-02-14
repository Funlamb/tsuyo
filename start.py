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
   print(posts)
   db.close()
   return render_template("index.html", posts=posts)

@app.route('/mike')
def mike():
   db = get_db_connection()
   query = """SELECT users.firstName, workouts.dateandtime, sets.*, exercises.name FROM users
      JOIN workouts ON users.id = workouts.userID JOIN sets ON workouts.id = sets.workoutID JOIN exercises ON
      sets.exerciseID = exercises.id WHERE users.id = 1"""
   posts = db.execute(query).fetchall()
   # Get all workout orginized
   # Split them by days
   # Split them by exercises
   # Give them to the .thml to sort nicly 
   db.close()
   return render_template("mike.html", posts=posts)

@app.route('/help')
def help():
   return "Helped"

if __name__ == '__main__':
   app.run()