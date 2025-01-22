from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")
    name = models.CharField(max_length=60)
    has_time = models.BooleanField(default=False)
    has_distance = models.BooleanField(default=False)
    distance_unit = models.CharField(max_length=2, choices=[("m","m"),("km","km")], null=True, blank=True)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workouts")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.DurationField(blank=True, null=True)
    distance = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    rpe = models.IntegerField()

    def clean(self):
        if self.date > date.today():
            raise ValidationError("Datumet kan inte vara i framtiden.")
        if not self.activity.has_time and self.time is not None:
            raise ValidationError("Tid kan inte sparas för denna aktivitet.")
        if not self.activity.has_distance and self.distance is not None:
            raise ValidationError("Distans kan inte sparas för denna aktivitet.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.activity.name} den {self.date}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    login_code = models.CharField(max_length=6, blank=True, null=True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

models.signals.post_save.connect(create_user_profile, sender=User)