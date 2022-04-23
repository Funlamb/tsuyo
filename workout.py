# Setup class to handle workout things

class Workout:
    db = None

    def __init__(self, id, user_id, date_time):
        self.id = id
        self.user_id = user_id
        self.date_time = date_time

    @staticmethod
    def get(id):
        worlout_result = Workout.db.execute("SELECT * FROM workouts WHERE id=?", [id]).fetchone()
        if worlout_result:
            return Workout(worlout_result[0], worlout_result[1],worlout_result[2])
        else:
            return None

    def get_id(self):
        return self.id

    def get_date_time(self):
        return self.date_time
    
    @staticmethod
    def get_workout_id(datetime, userID):
        """
        Gets the workout id from the database given the datetime and userID
        
        Returns None if one does not exist
        """
        workout_id = Workout.db.execute("SELECT id FROM workouts WHERE userID=? AND DateAndTime=?", [userID, datetime]).fetchone()
        if workout_id:
            return workout_id
        else:
            return None

    @staticmethod
    def create_workout(datetime, userID):
        """
        Create a workout using the datetime for the userID
        """
        Workout.db.execute("INSERT INTO workouts (userID, DateAndTime) VALUES (?,?)", [userID, datetime])
        Workout.db.commit()

    def __str__(self):
        return ("ID: " + str(self.id) + " Date Time: " + str(self.date_time))