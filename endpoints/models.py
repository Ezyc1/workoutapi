from django.db import models
from django.contrib.auth.models import User

class Activity(models.model):
    activity_name=models.CharField(max_length=100)
    activity_hasTime=models.BooleanField()
    activity_hasDistance=models.BooleanField()
    activity_hasDistanceUnit=models.Choices()
    activity_UserId=models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.activity_name


class Workout(models.model):
    workout_date=models.DateField()
    user_id=models.ForeignKey()
    activity_id=models.ForeignKey()
    workout_description=models.TextField()
    workout_time=models.DurationField()
    workout_distance=models.DecimalField()
    workout_rpe=models.IntegerField()
    
    def __str__(self):
        return self

