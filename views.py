from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Secret
from .forms import SecretForm
from django.http import HttpResponse
from .models import TodoItem
from django.shortcuts import render, redirect
from .forms import TodoForm
from .forms import TodoItemForm
from django.shortcuts import get_object_or_404
from .forms import PasswordEntryForm
from .models import PasswordEntry
from .models import DiaryEntry
from .forms import DiaryForm
from .utils import analyze_sentiment, get_suggestion
from datetime import datetime
from textblob import TextBlob  # For simple sentiment analysis
from django.utils import timezone





# AUTH VIEWS
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

# DASHBOARD & PAGES
@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def diary_view(request):
    return render(request, 'diary.html')

@login_required
def todo_view(request):
    return render(request, 'todo.html')

@login_required
def password_view(request):
    return render(request, 'passwords.html')

@login_required
def todo_list(request):
    return render(request, 'vault_app/todo_list.html')

@login_required
def password_vault(request):
    return render(request, 'vault_app/password_vault.html')

@login_required
def diary_ai(request):
    return render(request, 'vault_app/diary_ai.html')

# SECRET VAULT VIEWS
@login_required
def secret_dashboard(request):
    if request.method == 'POST':
        form = SecretForm(request.POST)
        if form.is_valid():
            secret = form.save(commit=False)
            secret.user = request.user
            secret.save()
            return redirect('secret_dashboard')
    else:
        form = SecretForm()

    secrets = Secret.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'vault_app/secret_dashboard.html', {
        'form': form,
        'secrets': secrets
    })

@login_required
def view_secret_vault(request):
    secrets = Secret.objects.filter(user=request.user)
    return render(request, 'view_secrets.html', {'secrets': secrets})

@login_required
def add_secret_vault(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        Secret.objects.create(user=request.user, title=title, content=content)
        return redirect('view_secret_vault')
    return render(request, 'add_secret.html')


def add_secret(request):
    # Your logic here
    return render(request, 'add_secret.html')
def add_todo(request):
    from django.http import HttpResponse
from .models import Todo

@login_required
def add_todo(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description', '')
        date = request.POST['date']
        Todo.objects.create(
            user=request.user,
            title=title,
            description=description,
            date=date
        )
        return redirect('todo_list')
    return render(request, 'add_todo.html')
@login_required                       #for to do list dont delete
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            TodoItem.objects.create(user=request.user, title=title)
            return redirect('todo_list')
    return render(request, 'vault_app/add_task.html')

@login_required
def todo_list(request):
    print("User:", request.user, "Authenticated:", request.user.is_authenticated)

    if request.method == 'POST':
        print("Form Submitted:", request.POST)  # 👈 Check if data is sent
        form = TodoItemForm(request.POST)
        if form.is_valid():
            print("Form is valid.")
            todo_item = form.save(commit=False)
            todo_item.user = request.user
            todo_item.save()
            return redirect('todo_list')
        else:
            print("Form is NOT valid.")
    else:
        form = TodoItemForm()

    items = TodoItem.objects.filter(user=request.user)
    return render(request, 'vault_app/todo_list.html', {'form': form, 'items': items})


@login_required
def delete_todo(request, pk):
    item = get_object_or_404(TodoItem, pk=pk, user=request.user)
    item.delete()
    return redirect('todo_list')
@login_required
def password_vault(request):
    if request.method == 'POST':
        form = PasswordEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('password_vault')
    else:
        form = PasswordEntryForm()

    entries = PasswordEntry.objects.filter(user=request.user)

    return render(request, 'vault_app/password_vault.html', {
        'form': form,
        'entries': entries
    })

def delete_password(request, password_id):
    password = get_object_or_404(PasswordEntry, id=password_id)
    password.delete()
    return redirect('password_vault')

def diary_ai(request):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if content:
            DiaryEntry.objects.create(content=content)
            return redirect("diary_ai")

    entries = DiaryEntry.objects.order_by('-created_at')
    return render(request, "vault_app/diary_ai.html", {"entries": entries})

def delete_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id)
    if request.method == "POST":
        entry.delete()
    return redirect("diary_ai")

def analyze_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id)
    content = entry.content
    date = entry.created_at


    # Analyze sentiment
    analysis = TextBlob(content)
    polarity = analysis.sentiment.polarity

    # Determine mood
    if polarity > 0.2:
        mood = "Positive"
    elif polarity < -0.2:
        mood = "Negative"
    else:
        mood = "Neutral"

    # Keywords-based suggestions
    content_lower = content.lower()
    suggestions = []

    keyword_suggestions = {
        "stress": "Try some deep breathing or take a walk in nature 🌿",
        "anxious": "Everything will be okay. You can write down what's bothering you 📝",
        "happy": "That’s awesome! Keep doing what makes you feel this way 😊",
        "sad": "It's okay to feel down. Call a friend or treat yourself with kindness ❤️",
        "tired": "Take some time to rest. Sleep and relaxation are important 😴",
        "bored": "Try a new hobby or explore something you've never done before 🎨",
        "excited": "Yay! Enjoy the moment and spread that positive energy 🎉",
        "love": "Love makes life beautiful. Hold on to those special moments 💖",
        "angry": "Pause. Breathe. Channel your anger into something productive 💪"
    }

    for keyword, suggestion in keyword_suggestions.items():
        if keyword in content_lower:
            suggestions.append(suggestion)

    # Default suggestion based on mood
    if not suggestions:
        if mood == "Positive":
            suggestions.append("Keep shining and spreading good vibes! 🌟")
        elif mood == "Negative":
            suggestions.append("Be gentle with yourself. Tough times don’t last. 🌈")
        else:
            suggestions.append("Reflect and take care of yourself today. 💚")

    return render(request, 'vault_app/analyze_entry.html', {
        'entry': entry,
        'mood': mood,
        'suggestions': suggestions,
        'date': date,
    })
def analyze_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, pk=entry_id)

    content = entry.content.lower()

    # Mood-based suggestion logic
    if any(word in content for word in ["sad", "bad", "depressed", "cry", "upset", "angry", "tired"]):
        suggestion = "You seem down. Take a deep breath, maybe go for a walk or talk to someone you trust."
    elif any(word in content for word in ["happy", "excited", "joy", "fun", "enjoyed", "great", "trip"]):
        suggestion = "That's great! Keep doing what brings you joy!"
    else:
        suggestion = "Keep reflecting — writing helps!"

    return render(request, 'vault_app/analyze_entry.html', {
        'entry': entry,
        'suggestion': suggestion
    })












