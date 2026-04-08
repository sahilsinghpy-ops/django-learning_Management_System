from django.urls import path
from .views import (
    CategoryListCreateView,
    CourseListCreateView, CourseDetailView,
    LessonListCreateView, LessonDetailView,
    EnrollmentListView, EnrollCourseView,
    ReviewListCreateView,teacher_dashboard,student_dashboard,all_courses_page,MyCourseListView,course_detail_page
)

urlpatterns = [
    # ← Dashboard pages FIRST before any <int:> patterns
    path('teacher/dashboard/', teacher_dashboard, name='teacher-dashboard'),
    path('student/dashboard/', student_dashboard, name='student-dashboard'),
    path('all/', all_courses_page, name='all-courses'),

    # Categories
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),

    # Courses
    path('', CourseListCreateView.as_view(), name='course-list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course-detail'),

    # Lessons
    path('<int:course_id>/lessons/', LessonListCreateView.as_view(), name='lesson-list'),
    path('<int:course_id>/lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),

    # Enrollment
    path('enrollments/', EnrollmentListView.as_view(), name='enrollment-list'),
    path('<int:course_id>/enroll/', EnrollCourseView.as_view(), name='enroll-course'),

    # Reviews
    path('my-courses/', MyCourseListView.as_view(), name='my-courses'),
    path('<int:course_id>/reviews/', ReviewListCreateView.as_view(), name='review-list'),

    

# Add at top of urlpatterns
path('detail/<int:course_id>/', course_detail_page, name='course-detail-page'),
]