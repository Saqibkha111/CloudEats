from django import forms
from .models import Dish
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'price', 'image', 'is_available']

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
# from django import forms
# from .models import Dish
# from django.contrib.auth.models import User
# # from django.contrib.auth.forms import UserCreationForm
# # from django.contrib.auth.models import User


# class DishForm(forms.ModelForm):
#     class Meta:
#         model = Dish
#         fields = ['name', 'price', 'description', 'image', 'is_available']
#         widgets = {
#             'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Dish name'}),
#             'description': forms.Textarea(attrs={'class':'form-control', 'rows':4, 'placeholder':'Short description'}),
#             'price': forms.NumberInput(attrs={'class':'form-control', 'step':'0.01'}),
#             'available': forms.CheckboxInput(attrs={'class':'form-check-input'}),
#         }

# class RegisterForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']
# # 
# # class DishForm(forms.ModelForm):
# #     class Meta:
# #         model = Dish
# #         fields = ['name', 'description', 'price', 'image', 'available']

# # class RegisterForm(UserCreationForm):
# #     email = forms.EmailField(required=True)
# #     class Meta:
# #         model = User
# #         fields = ('username', 'email', 'password1', 'password2')
