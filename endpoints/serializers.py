from rest_framework import serializers
from .models import Activity, Workout
from rest_framework.serializers import ModelSerializer
from .models import User

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'name', 'has_time', 'has_distance', 'distance_unit']

class WorkoutSerializer(serializers.ModelSerializer):
    activity = serializers.PrimaryKeyRelatedField(queryset=Activity.objects.all())

    class Meta:
        model = Workout
        fields = ['id', 'activity', 'date', 'time', 'distance', 'description', 'rpe']
        
class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["url", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}
        
    
    def create(self, validated_data):
        user = User(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user