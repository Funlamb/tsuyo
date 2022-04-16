import json

class Graph_set:

    def __init__(self, id, interval, resistance, set_number, workout_id, workout_date, exercise_id, ex_name):
        self.id = id
        self.interval = interval
        self.resistance = resistance
        self.set_number = set_number
        self.workout_id = workout_id
        self.workout_date = workout_date
        self.exercise_id = exercise_id
        self.exercise_name = ex_name

    def __iter__(self):
        yield from {
            "id": self.id,
            "interval": self.interval,
            "resistance": self.resistance,
            "set_number": self.set_number,
            "workout_id": self.workout_id,
            "workout_date": self.workout_date,
            "exercise_id": self.exercise_id,
            "exercise_name": self.exercise_name,
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return self.__str__()