from flask import Flask, redirect, render_template, request, session
from werkzeug.security import generate_password_hash

from helper import message, get_db_connection
import exercise as exer
from users import User

app = Flask(__name__)
app.secret_key = "toots"
User.db = get_db_connection()
database = get_db_connection()

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

@app.route('/user_index')
# @login_required
def user_index():
   if not session.get('userID'):
      return message("Must be logged in.")

   cur = User.db.cursor()
   userID = []
   userID.append(session['userID']) # needs to be in a list to use .execute
   query = """SELECT users.firstName, workouts.dateandtime, workouts.id, sets.*, exercises.name FROM users
      JOIN workouts ON users.id = workouts.userID JOIN sets ON workouts.id = sets.workoutID JOIN exercises ON
      sets.exerciseID = exercises.id WHERE users.id = ?"""
   posts_unsorted = cur.execute(query, userID).fetchall()

   # Get all the exercises
   exercises = []
   for e in posts_unsorted:
      temp_exercise = exer.Exercise(e['firstName'], e['interval'], e['resistance'], e['setNumber'], e['workoutID'], e['exerciseID'], e['dateandtime'], e['name'])
      exercises.append(temp_exercise)
   
   # Get all workout orginized
   posts_sorted_daily = []
   temp = []
   # Split them by days
   if not posts_unsorted:
      return render_template("index.html", name=session['name'])
      
   # print(posts_unsorted[0]["id"])
   workoutID = posts_unsorted[0]["id"]

   for p in posts_unsorted:
      if p["id"] != workoutID:
         posts_sorted_daily.append(temp)
         # print(daily_posts)
         temp = []
         workoutID = p["id"]
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
   # for daily in posts_sorted_daily:
   #    exerciseID = daily[0]['exerciseID'] # get the first exerciseID
   #    for exercise in daily:
   #       if exercise['exerciseID'] != exerciseID:
   #          day_temp.append(exercise_temp)
   #          exercise_temp = []
   #          exerciseID = exercise['exerciseID']
   #       exercise_temp.append(exercise)
   #    posts_sorted_exercise.append(exercise_temp)

   # Debugging to check if sorting all exercises
   # for day in posts_sorted_exercise:
   #    for d in day:
   #       print(d['dateandtime'])

   # Find the exercise
   # Put the exercise in a temp list
   # Add the exercise list to new daily post list
   # Add the daily post list to posts_sorted_exercise list

   # Give them to the .html to sort nicly 

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

@app.route('/settings', methods=['get', 'post'])
def settings():
   if not session.get('userID'):
      return message("Must be logged in.")

   if request.method == "GET":
      return render_template("settings.html")

   if request.method == "POST":
      user = User.get(session["email"])
      ls = {}
      ls['email'] = request.form.get("email")
      ls['last_name'] = request.form.get("last_name")
      ls['first_name'] = request.form.get("first_name")
      ls['date_of_birth'] = request.form.get("date_of_birth")
      ls['change_password'] = request.form.get("change_password")
      ls['confirm_password'] = request.form.get("confirm_password")
      ls['original_password'] = request.form.get("original_password")

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