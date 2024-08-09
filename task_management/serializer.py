from rest_framework import serializers
from .models import UserProfile, Task
from django.db.models import Count


class ProfileSerializer(serializers.ModelSerializer):
    role = serializers.EmailField(source="role.role_name")
    first_name = serializers.EmailField(source="user.first_name")
    last_name = serializers.EmailField(source="user.last_name")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'last_name', 'email', 'role')


class TaskSerializer(serializers.ModelSerializer):
    temperature = serializers.CharField(source="temperature.temperature_name")
    class Meta:
        model = Task
        fields = '__all__'

        # completed_tasks = Task.objects.filter(is_completed=True).values('title', 'assign_to__user__email',
        #                                                                 'assign_to__user__first_name').annotate(
        #     task_count=Count('assign_to'))

class TaskSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Task


class TaskSerializer3(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
