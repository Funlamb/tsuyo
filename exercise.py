
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

    @staticmethod
    def get_exercise_id(name):
        """
        Gets exercise id if one exists

        Returns None if it does not
        """
        exercise_id = Exercise.db.execute("SELECT id FROM exercises WHERE name=?", [name]).fetchone()
        if exercise_id:
            return exercise_id
        else:
            return None

    @staticmethod
    def create_exercise(name):
        Exercise.db.execute("INSERT INTO exercises (name) VALUES (?)", [name])
        Exercise.db.commit()
    
    def __str__(self):
        return ("Id: " + str(self.id) + " Name: " + self.name)