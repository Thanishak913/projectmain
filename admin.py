from django.contrib import admin
from .models import Todo
from .models import DiaryEntry   # vault_app/admin.py

admin.site.register(DiaryEntry)
admin.site.register(Todo)

