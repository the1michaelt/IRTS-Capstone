from rest_framework import serializers
from .models import Student_Course

class Student_CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student_Course
        fields = ['grade_received', 'credits_received']