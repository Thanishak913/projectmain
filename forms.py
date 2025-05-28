from django import forms
from .models import Secret
from .models import Todo
from .models import TodoItem
from .models import PasswordEntry

class SecretForm(forms.ModelForm):
    class Meta:
        model = Secret
        fields = ['content']  # ✅ Correct
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'date']
        widgets = {
               'title': forms.TextInput(attrs={'class': 'form-control'}),
               'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
}
class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ['title']
class PasswordEntryForm(forms.ModelForm):
    class Meta:
        model = PasswordEntry
        fields = ['website', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }
class DiaryForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'placeholder': 'How was your day today?'}),
        label="",
    )






