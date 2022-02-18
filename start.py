from crypt import methods
from pkgutil import extend_path
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from helper import message

import sqlite3

app = Flask(__name__)
app.secret_key = "toots"

def get_db_connection():
   db = sqlite3.connect("workout.db")
   db.row_factory = sqlite3.Row
   return db

@app.route('/')
def index():
   session.clear()
   return render_template("login.html")

@app.route('/login', methods=["GET", "POST"])
def login():
   # remove any prior session
   session.clear()
   if request.method == "POST":
      # check that a user name was submitted
      if not request.form.get("email"):
         # return a page stating no user name
         return message("Need an e-mail")

      # check that a password was submitted
      if not request.form.get("password"):
         # return a page stating no password
         return message("Need a password")

      db = get_db_connection()
      user = db.execute("SELECT * FROM users WHERE users.email = ?", [request.form.get("email")]).fetchall()

      # Check password
      print("Login")
      pwhash = user[0]['hash']
      password = request.form.get('password')
      password_check = check_password_hash(pwhash, password)
      db.close()
      if password_check:
         session['userID'] = user[0]['id']
         session['name'] = user[0]['firstName']
         return redirect("/user_index")
      return message("Wrong Password. Go to log in page to try again.")
      # test those feilds to see if any match the users database
      # record the userID in the session

@app.route('/user_index')
# @login_required
def user_index():
   if not session.get('userID'):
      return message("Must be logged in.")

   db = get_db_connection()
   cur = db.cursor()
   userID = []
   userID.append(session['userID']) # needs to be in a list to use .execute
   query = """SELECT users.firstName, workouts.dateandtime, workouts.id, sets.*, exercises.name FROM users
      JOIN workouts ON users.id = workouts.userID JOIN sets ON workouts.id = sets.workoutID JOIN exercises ON
      sets.exerciseID = exercises.id WHERE users.id = ?"""
   posts_unsorted = cur.execute(query, userID).fetchall()
   
   # Get all workout orginized
   posts_sorted_daily = []
   temp = []
   # Split them by days
   if not posts_unsorted:
      return render_template("index.html", name=session['name'])
      
   # print(posts_unsorted[0]["id"])
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
      posts_sorted_exercise.append(exercise_temp)

   # Debugging to check if sorting all exercises
   # for day in posts_sorted_exercise:
   #    for d in day:
   #       print(d['dateandtime'])

   # Find the exercise
   # Put the exercise in a temp list
   # Add the exercise list to new daily post list
   # Add the daily post list to posts_sorted_exercise list

   # Give them to the .html to sort nicly 

   db.close()
   return render_template("index.html", posts=posts_sorted_daily, name=session['name'])

@app.route('/register', methods=['GET', 'POST'])
def register():
   if request.method == "GET":
      return render_template("register.html")

   if request.method == "POST":
   #   <!-- Check First Name text box -->
      first_name = request.form.get("first_name")
      if not first_name:
         return message("Need to input a first name.")
   #   <!-- Check Last Name text box -->
      last_name = request.form.get("last_name")
      if not last_name:
         return message("Need to input a last name.")
   #   <!-- Check E-Mail text box -->
      email_address = request.form.get("email_address")
      if not email_address:
         return message("Need to input an e-mail address.")
   #   <!-- Check Date of Birth text box -->
      date_of_birth = request.form.get("date_of_birth")
      if not date_of_birth:
         return message("Need to input a date of birth.")
   #   <!-- Check Password text box -->
      password = request.form.get("password")
      if not password:
         return message("Need to input a password.")
   #   <!-- Check Confirm Password text box -->
      confirm_password = request.form.get("confirm_password")
      if not confirm_password:
         return message("Need to input a confermation password.")

      # Check if passwords match
      if password != confirm_password:
         return message("Password and Confirm Password does not match")
      
      print("Creating Row for user")
      db = get_db_connection()
      cur = db.cursor()
      ls = [last_name, first_name, email_address, date_of_birth, generate_password_hash(password)]
      cur.execute("INSERT INTO users (lastName, firstName, email, dateOfBirth, hash) VALUES (?, ?, ?, ?, ?)", ls)
      # cur.execute("create table lang (name, first_appeared)")
      db.commit() # Need to commit the changes or it will not save to the database
      db.close()
   return message("You successfully registered. Go ahead and log in on the log in page.")

   
@app.route('/logout')
def help():
   session.clear()
   return message("Logging Out")

if __name__ == '__main__':
   app.run()