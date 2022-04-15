import json

class ExerciseCollection:
    def __init__(self, big_lst):
        self.version = 1
        self.type = "exercise"
        self.big_lst = big_lst

    def __iter__(self):
        yield from {
            "version": self.version,
            "type": self.type,
        }.items()

    def __str__(self):
        return json.dumps(self.big_lst)

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        exercises = []
        for small_lst in self.big_lst:
            ex_name = small_lst[0].exercise_name
            exercise = {"name": ex_name,
                        "sets": []}
            for sm in small_lst:
                exercise["sets"].append(sm.__dict__)
            exercises.append(exercise)

        to_return = {"version": self.version, "type": self.type, "exercises": exercises}
        return to_return