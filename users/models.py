from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    RoleChoices = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )

    role = models.CharField(max_length=10, choices=RoleChoices, default='student')
    bio =models.TextField(blank=True)
    def __str__(self):
        return f'{self.username}   {self.role}'


