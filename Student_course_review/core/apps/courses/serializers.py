from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'price', 'level', 'instructor', 'instructor_name', 'avg_rating',
                  'total_reviews', 'created_at']
        


