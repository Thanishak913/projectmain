from django.urls import path
from . import views
from .views import diary_ai, delete_entry, analyze_entry
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('diary/', views.diary_view, name='diary'),
    path('todo/', views.todo_view, name='todo'),
    path('passwords/', views.password_view, name='passwords'),
    path('add_secret/', views.add_secret, name='add_secret'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('view/', views.view_secret_vault, name='view_secret_vault'),
    path('add/', views.add_secret_vault, name='add_secret_vault'),
    path('dashboard/', views.secret_dashboard, name='secret_dashboard'),
    path('dashboard/', views.add_secret, name='secret_dashboard'),
    path('todo/', views.todo_list, name='todo_list'),
    path('diary-ai/', views.diary_ai, name='diary_ai'),
    path('todo/add/', views.add_todo, name='add_todo'),
    path('todo/list/', views.todo_list, name='todo_list'),
    path('todo/add/', views.add_task, name='add_task'),
    path('todo/delete/<int:pk>/', views.delete_todo, name='delete_todo'),
    path('password-vault/', views.password_vault, name='password_vault'),
    path("diary-ai/", views.diary_ai, name="diary_ai"),
    path("delete-entry/<int:entry_id>/", delete_entry, name="delete_entry"),
    path("analyze-entry/<int:entry_id>/", analyze_entry, name="analyze_entry"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete-password/<int:password_id>/', views.delete_password, name='delete_password'),
]


