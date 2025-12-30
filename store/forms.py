from django import forms
from django.contrib.auth.models import User
from . models import FarmerProfile,CustomerProfile,Product

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('farmer','farmer'),('customer','customer')])

    class Meta:
        model = User
        fields = ['username','email','password']
    
class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model=FarmerProfile
        exclude =['user','is_verified']

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model=CustomerProfile
        exclude =['user']

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['category','name','description','price','stock','image']


class RatingForm(forms.Form):
    rating=forms.ChoiceField(choices=[(i,i) for i in range (1,6)],widget=forms.RadioSelect)