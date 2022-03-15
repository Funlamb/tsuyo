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
            return Ex_set(ex_set_result[0], ex_set_result[1],ex_set_result[2],ex_set_result[3],ex_set_result[4])
        else:
            return None