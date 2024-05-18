from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User


class StyleFormMixin:
    '''Класс стилизации формы.'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    '''Класс регистрации нового пользователя'''
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserProfileForm(StyleFormMixin, UserChangeForm):
    '''Класс изменения данных пользователя.'''
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'phone',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
