class Exercise:
    def __init__(self, firstName, intervals, resistance, setNumber, workoutID, exerciseID, workoutDate, exerciseName):
        self.firstName = firstName
        self.intervals = intervals
        self.resistance = resistance
        self.setNumber = setNumber
        self.woroutID = workoutID
        self.exerciseID = exerciseID
        self.workoutDate = workoutDate
        self.exerciseName = exerciseName

    def anounce(self):
        print ("First Name: " + self.firstName + " Name: " + self.exerciseName, " Set: ", self.setNumber, " Intervals: ", self.intervals, " Resistance: ", self.resistance)