from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'})
    )
    password_confirm = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور'})
    )

    class Meta:
        model = User
        fields = ['phone_number', 'username', 'full_name']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره موبایل'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام و نام خانوادگی'}),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError('این شماره موبایل قبلاً ثبت شده است.')
        return phone

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('این نام کاربری قبلاً گرفته شده است.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('رمز عبور و تکرار آن یکسان نیستند.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'group_manager'  # نقش مدیر گروه
        if commit:
            user.save()
        return user


from django import forms
from django.contrib.auth import authenticate
from .models import User


class UserLoginForm(forms.Form):
    login_field = forms.CharField(
        label='شماره موبایل یا نام کاربری',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره موبایل یا نام کاربری'})
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'})
    )

    def clean(self):
        cleaned_data = super().clean()
        login_field = cleaned_data.get('login_field')
        password = cleaned_data.get('password')

        if login_field and password:
            # تلاش برای پیدا کردن کاربر با شماره موبایل یا نام کاربری
            user = None
            if User.objects.filter(phone_number=login_field).exists():
                user = User.objects.get(phone_number=login_field)
            elif User.objects.filter(username=login_field).exists():
                user = User.objects.get(username=login_field)

            if user is None:
                raise forms.ValidationError('کاربری با این مشخصات یافت نشد.')

            # احراز هویت
            user = authenticate(username=user.phone_number, password=password)
            if user is None:
                raise forms.ValidationError('رمز عبور اشتباه است.')

            cleaned_data['user'] = user
        return cleaned_data
