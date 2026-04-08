from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Courses, Lessons, Enrollment, Review
from .serializers import (
    CategorySerializer, CourseSerializer,
    LessonSerializer, EnrollmentSerializer, ReviewSerializer
)
from .permissions import IsTeacherOrReadOnly

from django.shortcuts import render

def teacher_dashboard(request):
    return render(request, 'courses/teacher_dashboard.html')

def student_dashboard(request):
    return render(request, 'courses/student_dashboard.html')


def all_courses_page(request):
    return render(request, 'courses/all_course.html')


# ── Category Views ──────────────────────────────────────────
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ── Course Views ─────────────────────────────────────────────
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Courses.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Courses.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ── Lesson Views ─────────────────────────────────────────────
class LessonListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Only return lessons for the course in the URL
        course_id = self.kwargs['course_id']
        return Lessons.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs['course_id']
        course = Courses.objects.get(id=course_id)
        serializer.save(course=course)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Lessons.objects.filter(course_id=course_id)


# ── Enrollment Views ─────────────────────────────────────────
class EnrollmentListView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Each student only sees their own enrollments
        return Enrollment.objects.filter(student=self.request.user)


class EnrollCourseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id):
        course = Courses.objects.get(id=course_id)

        # Check if already enrolled
        if Enrollment.objects.filter(student=request.user, course=course).exists():
            return Response(
                {"error": "You are already enrolled in this course"},
                status=status.HTTP_400_BAD_REQUEST
            )

        enrollment = Enrollment.objects.create(student=request.user, course=course)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ── Review Views ─────────────────────────────────────────────
class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Review.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs['course_id']
        course = Courses.objects.get(id=course_id)
        serializer.save(student=self.request.user, course=course)



class MyCourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Courses.objects.filter(teacher=self.request.user)
    

def course_detail_page(request, course_id):
    return render(request, 'courses/course_detail.html')