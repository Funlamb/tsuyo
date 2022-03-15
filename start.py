from crypt import methods
import imp
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import generate_password_hash

from helper import message, get_db_connection

from user import User
from head_set import Head_set
from workout import Workout
from ex_set import Ex_set
from exercise import Exercise

app = Flask(__name__)
app.secret_key = "toots"

# Setup databases from all classes
database = get_db_connection()
User.db = database
Workout.db = database
Ex_set.db = database
Exercise.db = database

@app.route('/')
def index():
   session.clear()
   return render_template("login.html")

@app.route('/login', methods=["GET", "POST"])
def login():
   user = User.get("fun@gmail.com")
   session['userID'] = user.get_id()
   session['name'] = user.get_first_name()
   session['email'] = user.get_email()
   return redirect("/user_index")
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

      # Get user if one exists
      email = request.form.get("email")
      user = User.get(email)

      if not user: # If user does not exist send user error message
         return message("Invalid credentials")
      
      # Check passwork and send to user_index if correct
      password = request.form.get('password')
      if user.check_password(password):
         session['userID'] = user.get_id()
         session['name'] = user.get_first_name()
         session['email'] = user.get_email()
         return redirect("/user_index")
      # If password did not match give user error message
      return message("Invalid credentials")

@app.route('/begin_edit_set', methods=["POST"])
def begin_edit_set():
   set_id = request.form.get('edit-set')
   cur = User.db.cursor()
   s_id = []
   s_id.append(set_id)
   query = """SELECT users.firstName, workouts.dateandtime AS w_datetime, workouts.id as w_id, sets.id AS s_id, sets.interval AS s_interval, sets.resistance AS s_res,
      sets.setNumber AS s_setNum, sets.workoutID AS s_workID, sets.exerciseID AS s_exeID, exercises.name AS e_name FROM users
      JOIN workouts ON users.id = workouts.userID JOIN sets ON workouts.id = sets.workoutID JOIN exercises ON
      sets.exerciseID = exercises.id WHERE s_id = ?"""
   set_to_edit = cur.execute(query, s_id).fetchone()
   # print(set_to_edit['s_id'])
   return render_template("edit_set.html", set_to_edit=set_to_edit)

@app.route('/edit_set', methods=["POST"])
def edit_set():
   # get workout id
   # get exercise id
   # get set id
   # edit the set
   return message("Set edited successfully")

@app.route('/user_index')
# @login_required
def user_index():
   if not session.get('userID'):
      return message("Must be logged in.")

   cur = User.db.cursor()
   userID = []
   userID.append(session['userID']) # needs to be in a list to use .execute
   query = """SELECT users.firstName, workouts.dateandtime AS w_datetime, workouts.id as w_id, sets.id AS s_id, sets.interval AS s_interval, sets.resistance AS s_res,
      sets.setNumber AS s_setNum, sets.workoutID AS s_workID, sets.exerciseID AS s_exeID, exercises.name AS e_name FROM users
      JOIN workouts ON users.id = workouts.userID JOIN sets ON workouts.id = sets.workoutID JOIN exercises ON
      sets.exerciseID = exercises.id WHERE users.id = ? ORDER BY sets.id DESC"""
   exercises = cur.execute(query, userID).fetchall()

   # If there are zero exercises show the user there name
   if not exercises:
      return render_template("index.html", name=session['name'])

   # Get all the exercises in head_set class
   head_sets = []
   for ex in exercises:
      # make a head_set form all the exercises
      head_set = Head_set(Workout.get(ex['w_id']), Exercise.get(ex['s_exeID']), Ex_set.get(ex['s_id']))
      head_sets.append(head_set)
   
   # Split workouts into days
   workout_id = head_sets[0].get_workout().get_id()
   head_sets_by_days = []
   temp = []
   for i in head_sets:
      if workout_id != i.get_workout().get_id():
         head_sets_by_days.append(temp)
         temp = []
         temp.append(i)
         workout_id = i.get_workout().get_id()
      temp.append(i)

   exercise_id = head_sets[0].get_exercise().get_id()
   head_sets_by_days_and_exercises = []
   for i in head_sets_by_days:
      temp_day = []
      temp = []
      for j in i:
         if exercise_id != j.get_exercise().get_id():
           temp_day.append(temp)
           temp = []
           temp.append(j)
           exercise_id = j.get_exercise().get_id()
         temp.append(j) 
      head_sets_by_days_and_exercises.append(temp_day)
   for i in head_sets_by_days_and_exercises:
      print(len(i))
   # Get all workout orginized
   posts_sorted_daily = []
   temp = []

   return render_template("index.html", posts=posts_sorted_daily, name=session['name'])

@app.route('/exercise', methods=["GET", "POST"])
def exercise():
   if not session.get('userID'):
      return message("Need to be logged in")
   if request.method == "POST":
      dates = request.form.getlist("ndatetime[]")
      exercises = request.form.getlist("nExercise[]")
      set_numbers = request.form.getlist("nsetnumber[]")
      repetitions = request.form.getlist("nrep[]")
      resistances = request.form.getlist("nresistance[]")
      zippedExercises = zip(dates, exercises, set_numbers, repetitions, resistances)
      for exercises in zippedExercises:
         # Create workout day and time if one does not exist
         doesWorkoutExist = database.execute("SELECT id FROM workouts WHERE DateAndTime=? AND userID=?", (exercises[0], session['userID'])).fetchone()
         workoutID = -1
         if doesWorkoutExist is None:
            # Add a T to the datetime
            date_time_str = ''
            for i, v in enumerate(exercises[0]):
               if i == 10:
                  date_time_str += 'T'
               else:
                  date_time_str += v
            database.execute("INSERT INTO workouts (userID, DateAndTime) VALUES (?,?)", [session['userID'], date_time_str])
            workoutID = database.execute("SELECT id FROM workouts WHERE DateAndTime=? AND userID=?", (exercises[0], session['userID'])).fetchone()[0]
            database.commit()
         else:
            workoutID = doesWorkoutExist[0]
         
         # Create exercise if one does not exist
         word = ''.join(exercises[1])
         doesExerciseExist = database.execute("SELECT id FROM exercises WHERE name=?", [word]).fetchone()
         exerciseID = -1
         if doesExerciseExist is None:
            database.execute("INSERT INTO exercises (name) VALUES (?)", [word])
            exerciseID = database.execute("SELECT id FROM exercises WHERE name=?", [word]).fetchone()[0]
            database.commit()
         else:
            exerciseID = doesExerciseExist[0]
      
         # Create the set
         sql = "INSERT INTO sets (workoutID, exerciseID, setNumber, interval, resistance) VALUES (?, ?, ?, ?, ?)"
         database.execute(sql, [workoutID, exerciseID, exercises[2], exercises[3], exercises[4]])
         database.commit()
   return render_template("exercise.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
   if request.method == "GET":
      return render_template("register.html")

   if request.method == "POST":
   # Check First Name text box 
      first_name = request.form.get("first_name")
      if not first_name:
         return message("Need to input a first name.")
   # Check Last Name text box 
      last_name = request.form.get("last_name")
      if not last_name:
         return message("Need to input a last name.")
   # Check E-Mail text box 
      email_address = request.form.get("email_address")
      if not email_address:
         return message("Need to input an e-mail address.")
   # Check Date of Birth text box 
      date_of_birth = request.form.get("date_of_birth")
      if not date_of_birth:
         return message("Need to input a date of birth.")
   # Check Password text box 
      password = request.form.get("password")
      if not password:
         return message("Need to input a password.")
   # Check Confirm Password text box 
      confirm_password = request.form.get("confirm_password")
      if not confirm_password:
         return message("Need to input a confermation password.")

      # Check if passwords match
      if password != confirm_password:
         return message("Password and Confirm Password does not match")
      
      # Check for existing user with email address
      if User.get(email_address):
         return message("E-mail already in use")
      # Create the new user
      ls = [last_name, first_name, email_address, date_of_birth, generate_password_hash(password)]
      User.add_user(ls)
   return message("You successfully registered. Go ahead and log in on the log in page.")

@app.route('/settings', methods=['GET', 'POST'])
def settings():
   if not session.get('userID'):
      return message("Must be logged in.")

   if request.method == "GET":
      return render_template("settings.html")

   if request.method == "POST":
      user = User.get(session["email"])
      ls = {}
      ls['email'] = request.form.get("email")
      ls['last_name'] = request.form.get("last-name")
      ls['first_name'] = request.form.get("first_name")
      ls['date_of_birth'] = request.form.get("date-of-birth")
      ls['change_password'] = request.form.get("change-password")
      ls['confirm_password'] = request.form.get("confirm-password")
      ls['original_password'] = request.form.get("original-password")

      # Test the original password
      if user.change_user_data(ls) == 1:
         return message("Need correct original password")
      elif user.change_user_data(ls) == 2:
         return message("Changed passwords do not match")
      
      user = User.get(session['email'])
      session['name'] = user.get_first_name()
      return message("Successfully changed your settings")

    
@app.route('/logout')
def logout():
   session.clear()
   return message("Logged Out")

if __name__ == '__main__':
   app.run()