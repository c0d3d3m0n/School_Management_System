from rest_framework import serializers
from .models import Student, Result

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = "__all__"
        read_only_fields = ['student', 'subject', 'marks_obtained', 'full_marks', 'passing_marks', 'exam_type']  