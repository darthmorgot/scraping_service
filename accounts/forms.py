from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            user_data = User.objects.filter(email=email)
            if not user_data.exists():
                raise forms.ValidationError('Такого пользователя нет')
            if not check_password(password, user_data[0].password):
                raise forms.ValidationError('Неверный пароль')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Данный пользователь не активен')
        return super(UserLoginForm, self).clean(*args, **kwargs)
