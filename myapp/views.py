from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserVerificationForm, PasswordResetForm, UserProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegistrationForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.auth import logout


def login_view(request):
    form = LoginForm(request.POST or None)
    message = ''
    next_url = request.GET.get('next') or request.POST.get('next') or 'home' # handle GET and POST cases

    if request.method == 'POST':
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials') #message = 'Invalid credentials'
    return render(request, 'myapp/login.html', {'form': form, 'message': message, 'next': next_url})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            #form.save()
            user = form.save(commit=False)

            # If you're collecting extra fields not handled by UserCreationForm
            user.full_name = form.cleaned_data['full_name']
            user.date_of_birth = form.cleaned_data['date_of_birth']
            
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password1']) 
            user.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('register')  # Make sure 'login' is a valid URL name        
        else:
            messages.error(request, 'Please correct the errors.')
    else:
        form = RegistrationForm()

    return render(request, 'myapp/register.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'myapp/profile.html', {'user': request.user})


'''
def forgot_password_view(request):
    user_verified = False
    user = None

    if 'verified' in request.session:
        user_verified = True
        user_id = request.session.get('user_id')
        user = CustomUser.objects.filter(id=user_id).first()

    if request.method == 'POST':
        if not user_verified:
            verify_form = UserVerificationForm(request.POST)
            if verify_form.is_valid():
                username = verify_form.cleaned_data['username']
                full_name = verify_form.cleaned_data['full_name']
                dob = verify_form.cleaned_data['date_of_birth']
                try:
                    user = CustomUser.objects.get(username=username, full_name=full_name, date_of_birth=dob)
                    request.session['verified'] = True
                    request.session['user_id'] = user.id
                    return redirect('forgot_password')
                except CustomUser.DoesNotExist:
                    messages.error(request, "User details not found.")
        else:
            reset_form = PasswordResetForm(request.POST)
            if reset_form.is_valid() and user:
                user.set_password(reset_form.cleaned_data['new_password'])
                user.save()
                del request.session['verified']
                del request.session['user_id']
                messages.success(request, "Password updated successfully!")
                return redirect('login')
    else:
        verify_form = UserVerificationForm()
        reset_form = PasswordResetForm() if user_verified else None

    return render(request, 'myapp/forgot_password.html', {
        'verify_form': verify_form,
        'reset_form': reset_form,
        'user_verified': user_verified
    })


from django.shortcuts import render
from .forms import ForgotPasswordForm, ResetPasswordForm
from .models import CustomUser

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
from .forms import UserVerificationForm, PasswordResetForm
from django.contrib.auth.hashers import make_password

def forgot_password_view(request):
    verification_form = UserVerificationForm()
    reset_form = None

    if request.method == 'POST':
        if 'verify_user' in request.POST:
            verification_form = UserVerificationForm(request.POST)
            if verification_form.is_valid():
                username = verification_form.cleaned_data['username']
                full_name = verification_form.cleaned_data['full_name']
                dob = verification_form.cleaned_data['date_of_birth']

                try:
                    user = CustomUser.objects.get(username=username, full_name=full_name, date_of_birth=dob)
                    request.session['reset_user_id'] = user.id  # save user id in session
                    reset_form = PasswordResetForm()
                except CustomUser.DoesNotExist:
                    messages.error(request, "No user found with the provided details.")
        
        elif 'reset_password' in request.POST:
            reset_form = PasswordResetForm(request.POST)
            if reset_form.is_valid():
                user_id = request.session.get('reset_user_id')
                if user_id:
                    try:
                        user = CustomUser.objects.get(id=user_id)
                        user.password = make_password(reset_form.cleaned_data['new_password'])
                        user.save()
                        login_url = reverse('login')
                        messages.success(request,mark_safe(f'Password updated successfully! <a href="{ login_url }">Click here to login</a>'))

                        return redirect('forgot_password')
                    except CustomUser.DoesNotExist:
                        messages.error(request, "Something went wrong. Please try again.")
                else:
                    messages.error(request, "Session expired. Please start again.")
            verification_form = UserVerificationForm()  # Show again if password reset fails

    return render(request, 'myapp/forgot_password.html', {
        'verification_form': verification_form,
        'reset_form': reset_form
    })'''

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
from .forms import UserVerificationForm, PasswordResetForm
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.utils.safestring import mark_safe

def forgot_password_view(request):
    verification_form = UserVerificationForm()
    reset_form = None

    if request.method == 'POST':
        if 'verify_user' in request.POST:
            verification_form = UserVerificationForm(request.POST)
            if verification_form.is_valid():
                username = verification_form.cleaned_data['username']
                full_name = verification_form.cleaned_data['full_name']
                dob = verification_form.cleaned_data['date_of_birth']

                try:
                    user = CustomUser.objects.get(username=username, full_name=full_name, date_of_birth=dob)
                    request.session['reset_user_id'] = user.id
                    reset_form = PasswordResetForm()
                except CustomUser.DoesNotExist:
                    messages.error(request, "No user found with the provided details.")

        elif 'reset_password' in request.POST:
            reset_form = PasswordResetForm(request.POST)
            user_id = request.session.get('reset_user_id')

            if reset_form.is_valid():
                if user_id:
                    try:
                        user = CustomUser.objects.get(id=user_id)
                        user.set_password(reset_form.cleaned_data['new_password'])
                        user.save()
                        del request.session['reset_user_id']
                        login_url = reverse('login')
                        messages.success(request, mark_safe(f'Password updated successfully! <a href="{login_url}" style="color:whitesmoke; text-decoration:none;">Click here to login</a>'))
                        return redirect('forgot_password')
                    except CustomUser.DoesNotExist:
                        messages.error(request, "Something went wrong. Please try again.")
                else:
                    messages.error(request, "Session expired. Please start again.")
            else:
                # Re-populate verification form with previously verified user
                if user_id:
                    try:
                        user = CustomUser.objects.get(id=user_id)
                        verification_form = UserVerificationForm(initial={
                            'username': user.username,
                            'full_name': user.full_name,
                            'date_of_birth': user.date_of_birth,
                        })
                    except CustomUser.DoesNotExist:
                        verification_form = UserVerificationForm()

    else:
        # Initial GET request
        if 'reset_user_id' in request.session:
            reset_form = PasswordResetForm()

    return render(request, 'myapp/forgot_password.html', {
        'verification_form': verification_form,
        'reset_form': reset_form
    })


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'myapp/home.html')

@login_required
def besties_view(request):
    return render(request, 'myapp/besties.html')

@login_required
def add_bestie_view(request):
    return render(request, 'myapp/add_bestie.html')



@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
    
        print(request.user.full_name)
        print(request.user.date_of_birth)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'myapp/settings.html', {'form': form})
