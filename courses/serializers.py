from rest_framework import serializers
from django.db.models import Avg
from .models import Category, Courses, Lessons, Enrollment, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = ['id', 'course', 'title', 'content', 'video_url', 'order']


class ReviewSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.username')

    class Meta:
        model = Review
        fields = ['id', 'course', 'student', 'student_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['student','course']


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    teacher_name = serializers.ReadOnlyField(source='teacher.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Courses
        fields = [
            'id', 'teacher', 'teacher_name', 'category', 'category_name',
            'Title', 'Description', 'thumbnail', 'created_at',
            'lessons', 'reviews', 'average_rating'
        ]
        read_only_fields = ['teacher']

    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0


class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.ReadOnlyField(source='course.Title')
    student_name = serializers.ReadOnlyField(source='student.username')

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_name', 'course', 'course_title', 'created_at']
        read_only_fields = ['student']