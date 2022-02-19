class Exercise:
    def __init__(self, intervals, resistance, setNumber, workoutID, exerciseID, workoutDate, exerciseName):
        self.intervals = intervals
        self.resistance = resistance
        self.setNumber = setNumber
        self.woroutID = workoutID
        self.exerciseID = exerciseID
        self.workoutDate = workoutDate
        self.exerciseName = exerciseName

    def anounce(self):
        print ("Name: " + self.exerciseName, " Set: ", self.setNumber, " Intervals: ", self.intervals, " Resistance: ", self.resistance)