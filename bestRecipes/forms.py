from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Recipe
from .context_processors import dif_choices


class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Введите username'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={'class':'form-control', 'placeholder':'Введите почту'}))
    password1 = forms.CharField(label="Password", min_length=3, max_length=128,
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        help_text="<small>Введите пароль.</small>")
    password2 = forms.CharField(label="Password, again", min_length=3, max_length=128,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="<small>Введите ещё раз пароль.</small>")


class PostCreateForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Введите название блюда'}))
    categories = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',
        'placeholder':'Введите категории, разделенные пробелом. Пример: паста,суши'}))
    image = forms.ImageField(widget=forms.FileInput(
        attrs={'class':'form-control-file'}))
    cooking_time = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class':'form-control',
               'placeholder':'Введите приблизительное время готовки (в минутах)'}))
    difficulty = forms.ChoiceField(widget=forms.Select(
        attrs={'class':'form-control'}), choices=dif_choices)
    text = forms.CharField(widget=forms.Textarea(
        attrs={'class':'form-control'}))

    class Meta:
        model = Recipe
        fields = ['title', 'categories', 'image', 'cooking_time', 'difficulty', 'text']
