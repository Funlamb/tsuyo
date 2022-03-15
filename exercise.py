
class Exercise:
    db = None
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @staticmethod
    def get(id):
        exercise_result = Exercise.db.execute("SELECT * FROM exercises WHERE id=?", [id]).fetchone()
        if exercise_result:
            return Exercise(exercise_result[0], exercise_result[1])
        else:
            return None

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id