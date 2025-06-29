from datetime import datetime

class Workout:
    def __init__(self, exercise: str, duration: int, calories: int):
        self.date = datetime.now().strftime("%Y-%m-%d") # today's date
        self.time = datetime.now().strftime("%H:%M:%S") # current time
        self.exercise = exercise
        self.duration = duration
        self.calories = calories

    def to_dict(self):
        return {
            "date": self.date,
            "time": self.time,
            "exercise": self.exercise,
            "duration": self.duration,
            "calories": self.calories
        }