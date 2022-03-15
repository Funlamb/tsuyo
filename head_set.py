
class Head_set:
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