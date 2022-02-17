from pkgutil import extend_path
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

@app.route('/mike')
def mike():
   db = get_db_connection()
   query = """SELECT users.firstName, workouts.dateandtime, workouts.id, sets.*, exercises.name FROM users
      JOIN workouts ON users.id = workouts.userID JOIN sets ON workouts.id = sets.workoutID JOIN exercises ON
      sets.exerciseID = exercises.id WHERE users.id = 1"""
   posts_unsorted = db.execute(query).fetchall()
   
   # Get all workout orginized
   posts_sorted_daily = []
   temp = []
   # Split them by days
   workoutID = posts_unsorted[0]["id"]
   for p in posts_unsorted:
      if p['id'] != workoutID:
         posts_sorted_daily.append(temp)
         # print(daily_posts)
         temp = []
         workoutID = p['id']
      temp.append(p)   
   posts_sorted_daily.append(temp) # Adds the last day from the query
   temp = []
   
   # Split them by exercises
   posts_sorted_exercise = []
   # Take the posts_sorted_daily and sort them by exercise
   # Look at the daily post
   # Can't seem to figure out how to sort this list. Ask Steve is there is a term for what it is I'm trying to do. 
   day_temp = []
   exercise_temp = []
   for daily in posts_sorted_daily:
      exerciseID = daily[0]['exerciseID'] # get the first exerciseID
      for exercise in daily:
         if exercise['exerciseID'] != exerciseID:
            day_temp.append(exercise_temp)
            exercise_temp = []
            exerciseID = exercise['exerciseID']
         exercise_temp.append(exercise)
      day_temp.append(exercise_temp)
   for day in posts_sorted_exercise:
      for d in day:
         print(d['dateandtime'])
   # Find the exercise
   # Put the exercise in a temp list
   # Add the exercise list to new daily post list
   # Add the daily post list to posts_sorted_exercise list

   # Give them to the .html to sort nicly 

   db.close()
   return render_template("mike.html", posts=posts_sorted_daily)

@app.route('/help')
def help():
   return "Helped"

if __name__ == '__main__':
   app.run()