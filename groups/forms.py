from django import forms
from .models import Group

class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'province', 'city']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام گروه سرود'}),
            'province': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'استان'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شهر'}),
        }