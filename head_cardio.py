
class Head_cardio:
    """
    Main call to hold cardio data

    Workout holds date, and self.id

    Exercise holds name, and self.id

    Ex_set holds interval, resistance, set_number, workout_id, and exercise_id
    """
    def __init__(self, workout, exercise, ex_cardio):
        self.workout = workout
        self.exercise = exercise
        self.ex_cardio = ex_cardio
        pass

    def get_workout(self):
        return self.workout
    
    def get_exercise(self):
        return self.exercise
    
    def get_ex_set(self):
        return self.ex_cardio

    def __str__(self):
        text = ""
        text += self.exercise.__str__() + " "
        text += self.workout.__str__() + " "
        text += self.ex_cardio.__str__()
        return text