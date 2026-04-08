from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Courses(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    Title = models.CharField(max_length=100)
    Description = models.TextField()
    thumbnail = models.ImageField(upload_to='courses_thumbs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Title


class Lessons(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=100)
    content = models.TextField()
    video_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.course.Title} - {self.title}'


class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='enrollments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f'{self.student.username} enrolled in {self.course.Title}'


class Review(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Enter a number between 1 and 5'
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'student')

    def __str__(self):
        return f'{self.student.username} - {self.course.Title} ({self.rating} stars)'