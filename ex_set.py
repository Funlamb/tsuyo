# setup class to handle set things

class Ex_set:
    db = None

    def __init__(self, id, interval, resistance, set_number, workout_id, exercise_id):
        self.id = id
        self.interval = interval
        self.resistance = resistance
        self.set_number = set_number
        self.workout_id = workout_id
        self.exercise_id = exercise_id

    @staticmethod
    def get(id):
        ex_set_result = Ex_set.db.execute("SELECT * FROM sets WHERE id=?", [id]).fetchone()
        if ex_set_result:
            return Ex_set(ex_set_result[0], ex_set_result[1],ex_set_result[2],ex_set_result[3],ex_set_result[4], ex_set_result[5])
        else:
            return None
    
    @staticmethod
    def edit_set(interval, resistance, workout_id, exercise_id, set_id):
        query = """UPDATE sets SET interval=?, resistance=?, workoutID=?, exerciseID=? WHERE ID=?"""
        Ex_set.db.execute(query, [interval, resistance, workout_id, exercise_id, set_id])
        Ex_set.db.commit()

    @staticmethod
    def add_set(workout_id, exercise_id, exercises):
        sql = "INSERT INTO sets (workoutID, exerciseID, setNumber, interval, resistance) VALUES (?, ?, ?, ?, ?)"
        Ex_set.db.execute(sql, [workout_id, exercise_id, exercises[2], exercises[3], exercises[4]])
        Ex_set.db.commit()