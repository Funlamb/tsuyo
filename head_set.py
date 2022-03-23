
class Head_set:
    """
    Main call to hold workout data

    Workout holds date, and self.id

    Exercise holds name, and self.id

    Ex_set holds interval, resistance, set_number, workout_id, and exercise_id
    """
    def __init__(self, workout, exercise, ex_set):
        self.workout = workout
        self.exercise = exercise
        self.ex_set = ex_set
        pass

    def get_workout(self):
        return self.workout
    
    def get_exercise(self):
        return self.exercise
    
    def get_ex_set(self):
        return self.ex_set