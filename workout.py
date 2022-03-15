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