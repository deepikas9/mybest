from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=100, widget=forms.TextInput(attrs={'class': 'input','placeholder': 'Username'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'input','placeholder': 'Password'}))


class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Full Name'})
    )
    
    date_of_birth = forms.DateField(
        widget=forms.TextInput(attrs={
            #'type': 'date',
            'placeholder': 'Date of Birth (dd-mm-yyyy)',
            'class': 'form-control datepicker'

        }), required=False, input_formats=['%d-%m-%Y']
    )

  


    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email ID'}), required=True
    )
    
    # GENDER_CHOICES = [
    #     ('M', 'Male'), ('F', 'Female'), ('O', 'Other'),
    # ]
    # gender = forms.ChoiceField(
    #     choices=GENDER_CHOICES,
    #     widget=forms.RadioSelect
    # )
    
    # username = forms.CharField(
    #     max_length=50,
    #     widget=forms.TextInput(attrs={'placeholder': 'Choose a username'})
    # )
    
    # password = forms.CharField(
    #     widget=forms.PasswordInput(attrs={'placeholder': 'Enter a password'})
    # )
    
    # confirm_password = forms.CharField(
    #     widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'})
    # )
    class Meta:
        model = CustomUser
        fields = ['full_name', 'date_of_birth', 'email',  'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize widgets of inherited fields if needed
        self.fields['username'].widget.attrs.update({'placeholder': 'Choose a username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})

from django import forms

class UserVerificationForm(forms.Form):
    username = forms.CharField(label='username', max_length=100, widget=forms.TextInput(attrs={'class': 'input','placeholder': 'Your Username'}))
    
    #username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your Full Name'}))
    #date_of_birth = forms.TextInput(widget=forms.DateInput(attrs={'type': 'date','placeholder': 'Select your date of birth'}))
    date_of_birth = forms.DateField(
        widget=forms.TextInput(attrs={
            #'type': 'date',
            'placeholder': 'Date of Birth',
            'class': 'form-control datepicker'

        }), required=False, input_formats=['%d/%m/%Y'])

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}),label='New Password')
    confirm_password =  confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}), label='Confirm Password')

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get('new_password')
        pw2 = cleaned_data.get('confirm_password')
        if pw1 != pw2:
            raise forms.ValidationError("Passwords do not match")
        if pw1:
            validate_password(pw1)
        return cleaned_data
    

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'date_of_birth',  'email']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
             'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
              # assuming you're storing gender as text
        }
