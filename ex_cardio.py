
class Ex_cardio:
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
        ex_set_result = Ex_cardio.db.execute("SELECT * FROM cardios WHERE id=?", [id]).fetchone()
        if ex_set_result:
            return Ex_cardio(ex_set_result[0], ex_set_result[1],ex_set_result[2],ex_set_result[3],ex_set_result[4], ex_set_result[5])
        else:
            return None
    
    @staticmethod
    def add_cardio(duration, distance, workout_id, exercise_id):
        query = """INSERT INTO cardios (duration, distance, setNumber, workoutID, exerciseID) VALUES (?, ?, ?, ?, ?)"""
        Ex_cardio.db.execute(query, [duration, distance, 1, workout_id, exercise_id])
        Ex_cardio.db.commit()
    
    @staticmethod
    def edit_cario(duration, distance, workout_id, exercise_id, cardio_id):
        query = """UPDATE cardios SET duration=?, distance=?, workoutID=?, exerciseID=? WHERE ID=?"""
        Ex_cardio.db.execute(query, [duration, distance, workout_id, exercise_id, cardio_id])
        Ex_cardio.db.commit()

    def __str__(self) -> str:
        return ("ID: " + str(self.id) + " Duration: " + str(self.interval) + " Distance " + str(self.resistance))