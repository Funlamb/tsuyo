import os
from pickle import FALSE, TRUE
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import generate_password_hash

from helper import message, get_db_connection, default, login_required

from user import User
from head_set import Head_set
from workout import Workout
from ex_set import Ex_set
from ex_cardio import Ex_cardio
from exercise import Exercise
from graph_set import Graph_set
from ExerciseCollection import ExerciseCollection
from head_cardio import Head_cardio
import json

app = Flask(__name__)
app.secret_key = "toots"

# Select true to run on Heroku false to run local
running_heroku = FALSE 

# Setup databases from all classes
database = get_db_connection()
User.db = database
Workout.db = database
Ex_set.db = database
Exercise.db = database
Ex_cardio.db = database

@app.route('/select2')
def select2():
   return render_template("select2.html")

@app.route('/')
def index():
   session.clear()
   return render_template("login.html")

@app.route('/login', methods=["GET", "POST"])
def login():
   # This block used to temporaroly test site
   # user = User.get("funlamb@gmail.com")
   # session['user_id'] = user.get_id()
   # session['name'] = user.get_first_name()
   # session['email'] = user.get_email()

   # reset password for user
   # user = User.get("test@test.com") # input user's email address
   # ls = {}
   # ls['password'] = "test" # change password to this word
   # user.reset_password(ls)
   # return redirect("/list_workouts")
   
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
      
      # Check passwork and send to list_workouts if correct
      password = request.form.get('password')
      if user.check_password(password):
         session['user_id'] = user.get_id()
         session['name'] = user.get_first_name()
         session['email'] = user.get_email()
         return redirect("/list_workouts")
      # If password did not match give user error message
      return message("Invalid credentials")
   return render_template("login.html")

@app.route('/add_cardio', methods=["GET" ,"POST"])
@login_required
def add_cardio():
   if request.method == "GET":
      return render_template("add_cardio.html")
   # get relevent info
   duration = request.form.get('duration')
   distance = request.form.get('distance')

   # Get workout id, create a workout if one does not exist
   datetime = request.form.get('datetime')
   workout_id =  Workout.get_workout_id(datetime, session['user_id'])
   if workout_id:
      workout_id = workout_id[0]
   else:
      Workout.create_workout(datetime, session['user_id'])
      workout_id = Workout.get_workout_id(datetime, session['user_id'])[0]
   
   # Get exercise id, create one if one does not exist
   exercise = request.form.get('exercise')
   exercise_id = Exercise.get_exercise_id(exercise)
   if exercise_id:
      exercise_id = exercise_id[0]
   else:
      Exercise.create_exercise(exercise)
      exercise_id = Exercise.get_exercise_id(exercise)[0]

   # add row to database
   Ex_cardio.add_cardio(duration, distance, workout_id, exercise_id)
   return redirect("/list_cardio")

@app.route('/edit_cardio', methods=["POST"])
@login_required
def edit_cardio():
   cardio_id = request.form.get('edit-cardio')
   
   # Get workout id, create a workout if one does not exist
   datetime = request.form.get('datetime')
   workout_id =  Workout.get_workout_id(datetime, session['user_id'])
   if workout_id:
      workout_id = workout_id[0]
   else:
      Workout.create_workout(datetime, session['user_id'])
      workout_id = Workout.get_workout_id(datetime, session['user_id'])[0]
   
   # Get exercise id, create one if one does not exist
   name = request.form.get('e_name')
   exercise_id = Exercise.get_exercise_id(name)
   if exercise_id:
      exercise_id = exercise_id[0]
   else:
      Exercise.create_exercise(name)
      exercise_id = Exercise.get_exercise_id(name)[0]

   duration = request.form.get('c_duration')
   distance = request.form.get('c_dist')
   Ex_cardio.edit_cario(duration, distance, workout_id, exercise_id, cardio_id)
   return redirect("/list_cardio")

@app.route('/begin_edit_cardio', methods=['POST'])
@login_required
def begin_edit_cardio():
   # get cardio from database
   cur = database.cursor()
   cardio_id = request.form.get('edit-cardio')
   query = """SELECT users.firstName, workouts.dateandtime AS w_datetime, workouts.id as w_id, cardios.id AS c_id, cardios.duration AS c_duration, 
      cardios.distance AS c_dist, cardios.setNumber AS c_setNum, cardios.workoutID AS c_workID, cardios.exerciseID AS c_exeID, exercises.name AS e_name FROM users
      JOIN workouts ON users.id = workouts.userID JOIN cardios ON workouts.id = cardios.workoutID JOIN exercises ON
      cardios.exerciseID = exercises.id WHERE c_id = ?"""
   cardio_to_edit = cur.execute(query, [cardio_id]).fetchone()

   # pass information to page
   return render_template("edit_cardio.html", cardio_to_edit=cardio_to_edit)

@app.route('/list_cardio', methods=["GET", "POST"])
@login_required
def cardio_list():
   # get users cardio workouts
   cur = database.cursor()
   u_id = session['user_id']
   query = """SELECT users.firstName, workouts.dateandtime AS w_datetime, workouts.id AS w_id, cardios.id AS c_id, cardios.duration AS c_duration,
      cardios.distance AS c_distance, cardios.exerciseID AS c_exercise_id FROM users JOIN workouts ON users.id = workouts.userID JOIN cardios ON 
      workouts.id = cardios.workoutID JOIN exercises ON cardios.exerciseID = exercises.id WHERE users.id = ? ORDER BY workouts.dateandtime"""
   cardios = cur.execute(query, [u_id]).fetchall()
   # build cardio object
   head_cardios = []
   for i in cardios:
      temp = Head_cardio(Workout.get(i['w_id']), Exercise.get(i['c_exercise_id']), Ex_cardio.get(i['c_id']))
      head_cardios.append(temp)

   # orginize them by date
   all_workout_dates = [hs.get_workout().get_date_time() for hs in head_cardios]
   workout_date_dict = {d: {} for d in all_workout_dates}

   for hc in head_cardios:
      date = hc.get_workout().get_date_time()
      name = hc.get_exercise().get_name()
      duration = hc.get_ex_set().interval
      distance = hc.get_ex_set().resistance
      cardio_id = hc.get_ex_set().id
      if name in workout_date_dict[date]:
         workout_date_dict[date][name] += [duration, distance, cardio_id]
      else:
         workout_date_dict[date][name] = [duration, distance, cardio_id]
   
   single_workout_dates = sorted(workout_date_dict.keys(), reverse=True)
   # pass them to the page
   return render_template("cardio.html", dates=single_workout_dates, workouts=workout_date_dict)

@app.route('/graph', methods=["GET"])
@login_required
def graph():
   cur = database.cursor()
   u_id = session['user_id']
   # get the exercises the user has done
   query = """SELECT users.firstName, workouts.dateandtime AS w_datetime, workouts.id AS w_id, sets.id AS s_id, sets.interval AS s_interval, sets.resistance AS s_res,
      sets.setNumber AS s_setNum, sets.workoutID AS s_workID, sets.exerciseID AS s_exeID, exercises.name AS e_name FROM users
      JOIN workouts ON users.id = workouts.userID JOIN sets ON workouts.id = sets.workoutID JOIN exercises ON
      sets.exerciseID = exercises.id WHERE users.id = ? ORDER BY exercises.id"""
   exercises = cur.execute(query, [u_id]).fetchall()
   graph_exercises = []
   exercise_names = []
   for i in exercises:
      graph_exercises.append(Graph_set(i['s_id'], i['s_interval'], i['s_res'], i['s_setNum'], i['w_id'], i['w_datetime'], i['s_exeID'], i['e_name']))
      exercise_names.append(i['e_name'])
   
   unique_exercise_names = list(set(exercise_names))
   unique_exercise_names.sort()
   # find the first exercise of the exercises
   exercise_id = graph_exercises[0].exercise_id
   # start a small list
   big_lst = []
   small_lst = []
   graph_len = len(graph_exercises)
   for j, i in enumerate(graph_exercises):
      # add to small list til exercise changes
      if i.exercise_id == exercise_id:
         small_lst.append(i)
      else:
         # add small list to big list
         big_lst.append(small_lst)
         # start a new small list
         small_lst = []
         exercise_id = i.exercise_id
         small_lst.append(i)
      # catches edge case if there is only one exercise in the query
      if j == graph_len-1: 
         big_lst.append(small_lst)

   # exercises = {"Exercises": big_lst}
   exercise_col = ExerciseCollection(big_lst)
   json_exercise_col = json.dumps(exercise_col, default=default)
   # print(json_exercise_col)
   return render_template("graph.html", graph_exercises=json_exercise_col, dropdown_menu=unique_exercise_names)

@app.route('/begin_edit_set', methods=["POST"])
@login_required
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
   return render_template("edit_set.html", set_to_edit=set_to_edit)

@app.route('/edit_set', methods=["POST"])
@login_required
def edit_set():
   set_id = request.form.get('edit-set')
   
   # Get workout id, create a workout if one does not exist
   datetime = request.form.get('datetime')
   workout_id =  Workout.get_workout_id(datetime, session['user_id'])
   if workout_id:
      workout_id = workout_id[0]
   else:
      Workout.create_workout(datetime, session['user_id'])
      workout_id = Workout.get_workout_id(datetime, session['user_id'])[0]
   
   # Get exercise id, create one if one does not exist
   name = request.form.get('e_name')
   exercise_id = Exercise.get_exercise_id(name)
   if exercise_id:
      exercise_id = exercise_id[0]
   else:
      Exercise.create_exercise(name)
      exercise_id = Exercise.get_exercise_id(name)[0]

   interval = request.form.get('s_interval')
   resistance = request.form.get('s_res')
   Ex_set.edit_set(interval, resistance, workout_id, exercise_id, set_id)
   return redirect("/list_workouts")

@app.route('/list_workouts')
@login_required
def list_workouts():
   cur = User.db.cursor()
   userID = session['user_id']
   query = """SELECT users.firstName, workouts.dateandtime AS w_datetime, workouts.id as w_id, sets.id AS s_id, sets.interval AS s_interval, sets.resistance AS s_res,
      sets.setNumber AS s_setNum, sets.workoutID AS s_workID, sets.exerciseID AS s_exeID, exercises.name AS e_name FROM users
      JOIN workouts ON users.id = workouts.userID JOIN sets ON workouts.id = sets.workoutID JOIN exercises ON
      sets.exerciseID = exercises.id WHERE users.id = ? ORDER BY w_id DESC"""
   exercises = cur.execute(query, [userID]).fetchall()

   # If there are zero exercises show the user there name
   if not exercises:
      return render_template("list_workouts.html", name=session['name'])

   # Get all the exercises in head_set class
   head_sets = []
   for ex in exercises:
      # make a head_set form all the exercises
      head_set = Head_set(Workout.get(ex['w_id']), Exercise.get(ex['s_exeID']), Ex_set.get(ex['s_id']))
      head_sets.append(head_set)
   
   all_workout_dates = [hs.get_workout().get_date_time() for hs in head_sets]
   workout_date_dict = {d: {} for d in all_workout_dates}

   number_of_columns_for_table = 0
   for hs in head_sets:
      date = hs.get_workout().get_date_time()
      name = hs.get_exercise().get_name()
      interval = hs.get_ex_set().interval
      resistance = hs.get_ex_set().resistance
      set_id = hs.get_ex_set().id
      if name in workout_date_dict[date]:
         workout_date_dict[date][name] += [interval, resistance, set_id]
      else:
         workout_date_dict[date][name] = [interval, resistance, set_id]
      curr_columns = len(workout_date_dict[date][name])
      if curr_columns > number_of_columns_for_table:
         number_of_columns_for_table = curr_columns
   number_of_columns_for_table = int(number_of_columns_for_table / 3)

   single_workout_dates = sorted(workout_date_dict.keys(), reverse=True)

   return render_template("list_workouts.html", dates=single_workout_dates, workouts=workout_date_dict, columns=number_of_columns_for_table, name=session['name']) 

@app.route('/list_workouts_mobile')
@login_required
def list_workouts_mobile():
   cur = User.db.cursor()
   userID = session['user_id']
   query = """SELECT users.firstName, workouts.dateandtime AS w_datetime, workouts.id as w_id, sets.id AS s_id, sets.interval AS s_interval, sets.resistance AS s_res,
      sets.setNumber AS s_setNum, sets.workoutID AS s_workID, sets.exerciseID AS s_exeID, exercises.name AS e_name FROM users
      JOIN workouts ON users.id = workouts.userID JOIN sets ON workouts.id = sets.workoutID JOIN exercises ON
      sets.exerciseID = exercises.id WHERE users.id = ? ORDER BY w_id DESC"""
   exercises = cur.execute(query, [userID]).fetchall()

   # If there are zero exercises show the user there name
   if not exercises:
      return render_template("list_workouts_mobile.html", name=session['name'])

   # Get all the exercises in head_set class
   head_sets = []
   for ex in exercises:
      # make a head_set form all the exercises
      head_set = Head_set(Workout.get(ex['w_id']), Exercise.get(ex['s_exeID']), Ex_set.get(ex['s_id']))
      head_sets.append(head_set)
   
   all_workout_dates = [hs.get_workout().get_date_time() for hs in head_sets]
   workout_date_dict = {d: {} for d in all_workout_dates}

   number_of_columns_for_table = 0
   for hs in head_sets:
      date = hs.get_workout().get_date_time()
      name = hs.get_exercise().get_name()
      interval = hs.get_ex_set().interval
      resistance = hs.get_ex_set().resistance
      set_id = hs.get_ex_set().id
      if name in workout_date_dict[date]:
         workout_date_dict[date][name] += [interval, resistance, set_id]
      else:
         workout_date_dict[date][name] = [interval, resistance, set_id]
      curr_columns = len(workout_date_dict[date][name])
      if curr_columns > number_of_columns_for_table:
         number_of_columns_for_table = curr_columns
   number_of_columns_for_table = int(number_of_columns_for_table / 3)

   single_workout_dates = sorted(workout_date_dict.keys(), reverse=True)

   return render_template("list_workouts_mobile.html", dates=single_workout_dates, workouts=workout_date_dict, columns=number_of_columns_for_table, name=session['name']) 

@app.route('/add_set', methods=["GET", "POST"])
@login_required
def add_set():
   if request.method == "POST":
      dates = request.form.getlist("nDatetime[]")
      exercises = request.form.getlist("nExercise[]")
      set_numbers = request.form.getlist("nSetnumber[]")
      repetitions = request.form.getlist("nRep[]")
      resistances = request.form.getlist("nResistance[]")
      zippedExercises = zip(dates, exercises, set_numbers, repetitions, resistances)

      for exercises in zippedExercises:
         # Create workout day and time if one does not exist
         doesWorkoutExist = Workout.get_workout_id(exercises[0], session['user_id'])
         workout_id = -1
         if doesWorkoutExist is None:
            # Add a T to the datetime
            date_time_str = ''
            for i, v in enumerate(exercises[0]):
               if i == 10:
                  date_time_str += 'T'
               else:
                  date_time_str += v
            Workout.create_workout(date_time_str, session['user_id'])
            workout_id = Workout.get_workout_id(date_time_str, session['user_id'])[0]
         else:
            workout_id = doesWorkoutExist[0]
         
         # Create exercise if one does not exist
         word = ''.join(exercises[1])
         doesExerciseExist = Exercise.get_exercise_id(word)
         exercise_id = -1
         if doesExerciseExist is None:
            Exercise.create_exercise(word)
            exercise_id = Exercise.get_exercise_id(word)[0]
         else:
            exercise_id = doesExerciseExist[0]
      
         # Create the set
         Ex_set.add_set(workout_id, exercise_id, exercises)
      return redirect("/list_workouts")
   cur = User.db.cursor()
   query = "SELECT name FROM exercises"
   workout_list_sql = cur.execute(query).fetchall()
   workout_list = []
   for i in workout_list_sql:
      workout_list.append(i[0])
   sorted_workout_list = sorted(workout_list)
   # add list to actual exercise dropdown 
   return render_template("add_set.html", workout_list=sorted_workout_list)

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
@login_required
def settings():
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
   if (running_heroku == TRUE):
      port = int(os.getenv('PORT'))
      app.run(port=port)
   else:
      app.run(use_debugger=False, use_reloader=False, passthrough_errors=True)

   # Removed to run on gunicorn
   
   # Trying to get the debugger to work
   # https://www.youtube.com/watch?v=UXqiVe6h3lA&t=1194s
   # https://stackoverflow.com/questions/49171144/how-do-i-debug-flask-app-in-vs-code