from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
created_at = models.DateTimeField(default=timezone.now)

class Todo(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField()  # Date to schedule the task

    def __str__(self):
        return self.title
    class Secret(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        title = models.CharField(max_length=100)
        content = models.TextField()

        def __str__(self):
          return self.title

class Secret(models.Model):
    title = models.CharField(max_length=100, default="Untitled")
    content = models.TextField()
    # add other fields as needed

    def __str__(self):
        return self.title

class TodoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)  # <-- Add this
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
class PasswordEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    website = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)  # Encrypt later
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.website} ({self.username})"

class DiaryEntry(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
     



 



