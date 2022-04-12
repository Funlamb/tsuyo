import json

class ExerciseCollection:
    def __init__(self, exercises):
        self.version = 1
        self.type = "exercise"
        self.exercises2 = exercises

    def __iter__(self):
        yield from {
            "version": self.version,
            "type": self.type,
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        to_return = {"version": self.version, "type": self.type}
        exercises = {}
        for key, exercises2 in self.exercises2.items():
            i_exercises = []
            dict_exercise_types = {}
            for exercise in exercises2:
                j_exercises = []
                k = exercise[0].exercise_name
                for j in exercise:
                    j_exercises.append(j.__dict__)
                dict_exercise_types[k] = j_exercises
                i_exercises.append(dict_exercise_types)
            exercises[key] = i_exercises

        to_return["Exercises"] = exercises
        return to_return