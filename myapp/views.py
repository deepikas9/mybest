from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserVerificationForm, PasswordResetForm, UserProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegistrationForm
from .models import CustomUser, BestieRequest
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.auth import logout
from .forms import BestieSearchForm
from django.db.models import Q


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


@login_required
def search_bestie(request):
    form = BestieSearchForm(request.GET or None)
    results = []

    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            results = CustomUser.objects.filter(username__icontains=query).exclude(id=request.user.id).order_by('username')

    sent_requests = BestieRequest.objects.filter(from_user=request.user, status='pending')
    received_requests = BestieRequest.objects.filter(to_user=request.user, status='pending')

    accepted_requests_from_me = BestieRequest.objects.filter(from_user=request.user, status='accepted')
    accepted_requests_to_me = BestieRequest.objects.filter(to_user=request.user, status='accepted')

    # Get all accepted besties (from either side)
    accepted_user_ids = set()
    accepted_user_ids.update(accepted_requests_from_me.values_list('to_user_id', flat=True))
    accepted_user_ids.update(accepted_requests_to_me.values_list('from_user_id', flat=True))
    besties = CustomUser.objects.filter(id__in=accepted_user_ids)

    results_with_status = []
    for user in results:
        sent_req = sent_requests.filter(to_user=user).first()
        received_req = received_requests.filter(from_user=user).first()
        is_bestie = user in besties

        results_with_status.append({
            'user': user,
            'is_bestie': is_bestie,
            'sent_request': sent_req,
            'received_request': received_req,
        })

    return render(request, 'myapp/search_bestie.html', {
        'form': form,
        'results': results_with_status,
        'current_path': request.get_full_path(),
    })

'''

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, BestieRequest
from .forms import BestieSearchForm


@login_required
def search_bestie(request):
    form = BestieSearchForm(request.GET or None)
    results = []

    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            results = CustomUser.objects.filter(username__icontains=query).exclude(id=request.user.id).order_by('username')

    sent_requests = BestieRequest.objects.filter(from_user=request.user, status='pending')
    received_requests = BestieRequest.objects.filter(to_user=request.user, status='pending')

    accepted_requests_from_me = BestieRequest.objects.filter(from_user=request.user, status='accepted')
    accepted_requests_to_me = BestieRequest.objects.filter(to_user=request.user, status='accepted')

    # Get all accepted besties (from either side)
    accepted_user_ids = set()
    accepted_user_ids.update(accepted_requests_from_me.values_list('to_user_id', flat=True))
    accepted_user_ids.update(accepted_requests_to_me.values_list('from_user_id', flat=True))
    besties = CustomUser.objects.filter(id__in=accepted_user_ids)

    results_with_status = []
    for user in results:
        sent_req = sent_requests.filter(to_user=user).first()
        received_req = received_requests.filter(from_user=user).first()
        is_bestie = user in besties

        results_with_status.append({
            'user': user,
            'is_bestie': is_bestie,
            'sent_request': sent_req,
            'received_request': received_req,
        })

    return render(request, 'myapp/search_bestie.html', {
        'form': form,
        'results': results_with_status,
    })
'''

@login_required
def add_bestie(request, user_id):
    if request.method == 'POST':
        to_user = get_object_or_404(CustomUser, id=user_id)
        from_user = request.user
        if to_user != from_user:
            existing_request = BestieRequest.objects.filter(from_user=from_user, to_user=to_user).first()
            if existing_request:
                if existing_request.status == 'pending':
                    messages.info(request, f'You already sent a bestie request to {to_user.username}.')
                elif existing_request.status == 'accepted':
                    messages.info(request, f'{to_user.username} is already your bestie.')
            else:
                mutual_request = BestieRequest.objects.filter(from_user=to_user, to_user=from_user, status='pending').first()
                if mutual_request:
                    mutual_request.status = 'accepted'
                    mutual_request.save()
                    messages.success(request, f'Bestie request from {to_user.username} accepted automatically!')
                else:
                    BestieRequest.objects.create(from_user=from_user, to_user=to_user)
                    messages.success(request, f'Bestie request sent to {to_user.username}.')
    next_url = request.POST.get('next', 'search_bestie')
    return redirect(next_url)


@login_required
def accept_bestie(request, user_id):
    if request.method == 'POST':
        from_user = get_object_or_404(CustomUser, id=user_id)
        to_user = request.user

        bestie_request = BestieRequest.objects.filter(from_user=from_user, to_user=to_user, status='pending').first()
        if bestie_request:
            bestie_request.status = 'accepted'
            bestie_request.save()
            messages.success(request, f'You and {from_user.username} are now besties!')
        else:
            messages.error(request, 'No pending request found.')
    next_url = request.POST.get('next', 'search_bestie')
    return redirect(next_url)


@login_required
def bestie_list(request):
    besties = request.user.besties()
    return render(request, 'myapp/bestie_list.html', {
        'besties': besties
    })


@login_required
def remove_bestie(request, user_id):
    if request.method == 'POST':
        bestie = get_object_or_404(CustomUser, id=user_id)
        # Remove accepted requests from both sides to "remove" bestie relationship
        BestieRequest.objects.filter(from_user=request.user, to_user=bestie, status='accepted').delete()
        BestieRequest.objects.filter(from_user=bestie, to_user=request.user, status='accepted').delete()
        messages.success(request, f'{bestie.username} has been removed from your besties.')
    return redirect('bestie_list')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, BestieRequest
from .forms import BestieSearchForm


@login_required
def search_bestie(request):
    form = BestieSearchForm(request.GET or None)
    results = []

    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            results = CustomUser.objects.filter(username__icontains=query).exclude(id=request.user.id).order_by('username')

    sent_requests = BestieRequest.objects.filter(from_user=request.user, status='pending')
    received_requests = BestieRequest.objects.filter(to_user=request.user, status='pending')

    accepted_requests_from_me = BestieRequest.objects.filter(from_user=request.user, status='accepted')
    accepted_requests_to_me = BestieRequest.objects.filter(to_user=request.user, status='accepted')

    # Get all accepted besties (from either side)
    accepted_user_ids = set()
    accepted_user_ids.update(accepted_requests_from_me.values_list('to_user_id', flat=True))
    accepted_user_ids.update(accepted_requests_to_me.values_list('from_user_id', flat=True))
    besties = CustomUser.objects.filter(id__in=accepted_user_ids)

    results_with_status = []
    for user in results:
        sent_req = sent_requests.filter(to_user=user).first()
        received_req = received_requests.filter(from_user=user).first()
        is_bestie = user in besties

        results_with_status.append({
            'user': user,
            'is_bestie': is_bestie,
            'sent_request': sent_req,
            'received_request': received_req,
        })

    return render(request, 'myapp/search_bestie.html', {
        'form': form,
        'results': results_with_status,
    })


# @login_required
# def add_bestie(request, user_id):
#     if request.method == 'POST':
#         to_user = get_object_or_404(CustomUser, id=user_id)
#         from_user = request.user
#         if to_user != from_user:
#             existing_request = BestieRequest.objects.filter(from_user=from_user, to_user=to_user).first()
#             if existing_request:
#                 if existing_request.status == 'pending':
#                     messages.info(request, f'You already sent a bestie request to {to_user.username}.')
#                 elif existing_request.status == 'accepted':
#                     messages.info(request, f'{to_user.username} is already your bestie.')
#             else:
#                 mutual_request = BestieRequest.objects.filter(from_user=to_user, to_user=from_user, status='pending').first()
#                 if mutual_request:
#                     mutual_request.status = 'accepted'
#                     mutual_request.save()
#                     messages.success(request, f'Bestie request from {to_user.username} accepted automatically!')
#                 else:
#                     BestieRequest.objects.create(from_user=from_user, to_user=to_user)
#                     messages.success(request, f'Bestie request sent to {to_user.username}.')
#     next_url = request.POST.get('next', 'search_bestie')
#     return redirect(next_url)


@login_required
def accept_bestie(request, user_id):
    if request.method == 'POST':
        from_user = get_object_or_404(CustomUser, id=user_id)
        to_user = request.user

        bestie_request = BestieRequest.objects.filter(from_user=from_user, to_user=to_user, status='pending').first()
        if bestie_request:
            bestie_request.status = 'accepted'
            bestie_request.save()
            messages.success(request, f'You and {from_user.username} are now besties!')
        else:
            messages.error(request, 'No pending request found.')
    next_url = request.POST.get('next', 'search_bestie')
    return redirect(next_url)


@login_required
def bestie_list(request):
    besties = request.user.besties()
    return render(request, 'myapp/bestie_list.html', {
        'besties': besties
    })


@login_required
def remove_bestie(request, user_id):
    if request.method == 'POST':
        bestie = get_object_or_404(CustomUser, id=user_id)
        # Remove accepted requests from both sides to "remove" bestie relationship
        BestieRequest.objects.filter(from_user=request.user, to_user=bestie, status='accepted').delete()
        BestieRequest.objects.filter(from_user=bestie, to_user=request.user, status='accepted').delete()
        messages.success(request, f'{bestie.username} has been removed from your besties.')
    return redirect('bestie_list')


from django.shortcuts import redirect, get_object_or_404

# @login_required
# def add_bestie(request, user_id):
#     if request.method == 'POST':
#         bestie = get_object_or_404(CustomUser, id=user_id)
#         if bestie != request.user:
#             request.user.besties.add(bestie)
#     return redirect('search_bestie')  # name of the search view in urls.py


'''
@login_required
def add_bestie(request, user_id):
    if request.method == 'POST':
        bestie = get_object_or_404(CustomUser, id=user_id)
        if bestie != request.user:
            request.user.besties.add(bestie)
    next_url = request.POST.get('next', 'search_bestie')
    return redirect(next_url)
'''


@login_required
def add_bestie(request, user_id):
    if request.method == 'POST':
        to_user = get_object_or_404(CustomUser, id=user_id)
        from_user = request.user
        if to_user != from_user:
            # Check if a request or relationship already exists
            existing_request = BestieRequest.objects.filter(from_user=from_user, to_user=to_user).first()
            if existing_request:
                if existing_request.status == 'pending':
                    messages.info(request, f'You already sent a bestie request to {to_user.username}.')
                elif existing_request.status == 'accepted':
                    messages.info(request, f'{to_user.username} is already your bestie.')
            else:
                # Also check if to_user has sent a request to from_user (mutual request)
                mutual_request = BestieRequest.objects.filter(from_user=to_user, to_user=from_user, status='pending').first()
                if mutual_request:
                    # Accept mutual request automatically and create bestie relationship
                    mutual_request.status = 'accepted'
                    mutual_request.save()
                    messages.success(request, f'Bestie request from {to_user.username} accepted automatically!')

                    # Optionally create reciprocal accepted request or handle M2M besties
                else:
                    BestieRequest.objects.create(from_user=from_user, to_user=to_user)
                    messages.success(request, f'Bestie request sent to {to_user.username}.')
    next_url = request.POST.get('next', 'search_bestie')
    return redirect(next_url)


@login_required
def accept_bestie(request, user_id):
    if request.method == 'POST':
        from_user = get_object_or_404(CustomUser, id=user_id)
        to_user = request.user

        bestie_request = BestieRequest.objects.filter(from_user=from_user, to_user=to_user, status='pending').first()
        if bestie_request:
            bestie_request.status = 'accepted'
            bestie_request.save()

            # Optionally create reciprocal accepted request
            # BestieRequest.objects.create(from_user=to_user, to_user=from_user, status='accepted')

            messages.success(request, f'You and {from_user.username} are now besties!')
        else:
            messages.error(request, 'No pending request found.')
    next_url = request.POST.get('next', 'search_bestie')
    return redirect(next_url)




@login_required
def bestie_list(request):
    #   besties = request.user.besties.all()
    besties = request.user.besties()  # Note the parentheses to call the method

    return render(request, 'myapp/bestie_list.html', {
        'besties': besties
    })


'''
@login_required
def remove_bestie(request, user_id):
    if request.method == 'POST':
        bestie = get_object_or_404(CustomUser, id=user_id)
        request.user.besties.remove(bestie)
    return redirect('bestie_list')
'''

@login_required
def bestie_inbox(request):
    received_requests = BestieRequest.objects.filter(to_user=request.user, status='pending').select_related('from_user')

    return render(request, 'myapp/home.html', {
        'received_requests': received_requests,
    })