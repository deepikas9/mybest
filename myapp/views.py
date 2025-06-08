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
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import JsonResponse




#----------------------------------------Login ---------------------------------------------
def login_view(request):
    form = LoginForm(request.POST or None)
    next_url = request.GET.get('next') or request.POST.get('next') or 'home' # handle GET and POST cases

    # ✅ Show message if session was logged out
    if request.GET.get('session_expired') == '1':
        messages.info(request, "Your session was logged out.....")

    if request.method == 'POST':
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid credentials') #message = 'Invalid credentials'
                #messages.info(request, "Your session was logged out.")
    return render(request, 'myapp/login.html', {'form': form,   'next': next_url})






#----------------------------------------Register ---------------------------------------------
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






#----------------------------------------Forgot Password ---------------------------------------------
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





#----------------------------------------Logout ---------------------------------------------
def logout_view(request):
    # Clear all messages before logout
    list(messages.get_messages(request))  # 💥 Clear all session data completely
    logout(request)          # Log the user out
    return redirect('login')





#----------------------------------------Home -----------------------------------------------


@login_required
def add_bestie_view(request):
    return render(request, 'myapp/add_bestie.html')


#=======================================================================================================================
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



#=======================================================================================================================
@login_required
def search_bestie(request):
    form = BestieSearchForm(request.GET or None)
    results = []
    active_tab = request.GET.get('tab', 'search')  # 'search', 'sent', or 'received'

    if form.is_valid() and active_tab == 'search':
        query = form.cleaned_data.get('query')
        if query:
            results = CustomUser.objects.filter(username__icontains=query).exclude(id=request.user.id).order_by('username')

    sent_requests = BestieRequest.objects.filter(from_user=request.user, status='pending')
    received_requests = BestieRequest.objects.filter(to_user=request.user, status='pending')

    accepted_requests_from_me = BestieRequest.objects.filter(from_user=request.user, status='accepted')
    accepted_requests_to_me = BestieRequest.objects.filter(to_user=request.user, status='accepted')

    accepted_user_ids = set()
    accepted_user_ids.update(accepted_requests_from_me.values_list('to_user_id', flat=True))
    accepted_user_ids.update(accepted_requests_to_me.values_list('from_user_id', flat=True))
    besties = CustomUser.objects.filter(id__in=accepted_user_ids)

    results_with_status = []
    if active_tab == 'search':
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
        'sent_requests': sent_requests,
        'received_requests': received_requests,
        'active_tab': active_tab,
        'current_path': request.get_full_path(),
    })


#=======================================================================================================================
@login_required
def bestie_list(request):
    besties = request.user.besties()
    return render(request, 'myapp/bestie_list.html', {
        'besties': besties
    })



#=======================================================================================================================
@login_required
def remove_bestie(request, user_id):
    if request.method == 'POST':
        bestie = get_object_or_404(CustomUser, id=user_id)
        # Remove accepted requests from both sides to "remove" bestie relationship
        BestieRequest.objects.filter(from_user=request.user, to_user=bestie, status='accepted').delete()
        BestieRequest.objects.filter(from_user=bestie, to_user=request.user, status='accepted').delete()
        messages.success(request, f'{bestie.username} has been removed from your besties.')
    return redirect('bestie_list')




#===================================================================================================================
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
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('search_bestie')
    # If next_url is safe and valid, use it; otherwise, reverse to fallback URL name
    if not next_url or not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = reverse('search_bestie')
    return redirect(next_url)





#===================================================================================================================
@login_required
def bestie_inbox(request):
    received_requests = BestieRequest.objects.filter(to_user=request.user, status='pending').select_related('from_user')

    return render(request, 'myapp/home.html', {
        'received_requests': received_requests,
    })




#==================================================================================================================
@login_required
def add_bestie(request, user_id):
    if request.method == 'POST':
        to_user = get_object_or_404(CustomUser, id=user_id)
        from_user = request.user

        if to_user != from_user:
            existing_request = BestieRequest.objects.filter(from_user=from_user, to_user=to_user).first()

            if existing_request:
                if existing_request.status == 'pending':
                    msg = f'You already sent a bestie request to {to_user.username}.'
                    if request.headers.get("x-requested-with") == "XMLHttpRequest":
                        return JsonResponse({'status': 'exists', 'message': msg}, status=200)
                    messages.info(request, msg)
                elif existing_request.status == 'accepted':
                    msg = f'{to_user.username} is already your bestie.'
                    if request.headers.get("x-requested-with") == "XMLHttpRequest":
                        return JsonResponse({'status': 'already', 'message': msg}, status=200)
                    messages.info(request, msg)

            else:
                mutual_request = BestieRequest.objects.filter(from_user=to_user, to_user=from_user, status='pending').first()
                if mutual_request:
                    mutual_request.status = 'accepted'
                    mutual_request.save()
                    msg = f'Bestie request from {to_user.username} accepted automatically!'
                    if request.headers.get("x-requested-with") == "XMLHttpRequest":
                        return JsonResponse({'status': 'accepted', 'message': msg}, status=200)
                    messages.success(request, msg)
                else:
                    BestieRequest.objects.create(from_user=from_user, to_user=to_user)
                    msg = f'Bestie request sent to {to_user.username}.'
                    if request.headers.get("x-requested-with") == "XMLHttpRequest":
                        return JsonResponse({'status': 'sent', 'message': msg}, status=201)
                    messages.success(request, msg)

    # Normal fallback redirect (for non-AJAX)
    #next_url = request.POST.get('next', 'search_bestie')
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('search_bestie')
    return redirect(next_url)




#=================================================================================================================
@require_POST
@login_required
def cancel_bestie_request(request, user_id):
    to_user = get_object_or_404(CustomUser, id=user_id)
    from_user = request.user

    bestie_request = BestieRequest.objects.filter(from_user=from_user, to_user=to_user, status='pending').first()
    if bestie_request:
        bestie_request.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        messages.success(request, 'Bestie request canceled.')
    else:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False}, status=404)
        messages.error(request, 'No pending request to cancel.')
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('search_bestie')
    return redirect(next_url)





#==========================upto date no need to delete===================
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import CustomUser, ChatMessage

@login_required
def home_view(request):
    user = request.user
    query = request.GET.get('q', '')

    # Get accepted besties
    besties = user.besties()
    if query:
        besties = besties.filter(Q(username__icontains=query) | Q(full_name__icontains=query))

    # Build conversations list
    conversations = []
    for bestie in besties:
        last_msg = ChatMessage.objects.filter(
            Q(sender=user, receiver=bestie) | Q(sender=bestie, receiver=user)
        ).order_by('-timestamp').first()

        conversations.append({
            'username': bestie.username,
            'full_name': bestie.full_name or bestie.username,
            'photo_url': bestie.photo.url if bestie.photo else '/static/images/default.png',
            'last_message': last_msg.message if last_msg else '',
            'last_message_time': last_msg.timestamp if last_msg else '',
        })

    return render(request, 'myapp/home.html', {
        'user': user,
        'conversations': conversations,
        'query': query,
    })


# @login_required
# def chat_view(request, username):
#     user = request.user
#     bestie = get_object_or_404(CustomUser, username=username)

#     # Ensure they are besties
#     if bestie not in user.besties():
#         return render(request, 'chat_not_allowed.html', {'bestie': bestie})

#     if request.method == 'POST':
#         message = request.POST.get('message', '').strip()
#         if message:
#             ChatMessage.objects.create(sender=user, receiver=bestie, message=message)
#         return redirect('chat', username=username)

#     messages = ChatMessage.objects.filter(
#         Q(sender=user, receiver=bestie) | Q(sender=bestie, receiver=user)
#     ).order_by('timestamp')

#     return render(request, 'myapp/chat.html', {
#         'user': user,
#         'bestie': bestie,
#         'messages': messages,
#     })


'''
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CustomUser, ChatMessage

@login_required
def chat_view(request, username):
    user = request.user
    bestie = get_object_or_404(CustomUser, username=username)

    # Ensure they are besties
    if bestie not in user.besties():
        return render(request, 'not_allowed.html')

    if request.method == "POST":
        message = request.POST.get('message')
        if message:
            ChatMessage.objects.create(sender=user, receiver=bestie, message=message)
        return redirect('chat', username=bestie.username) 

    # All messages between user and bestie
    # messages = ChatMessage.objects.filter(
    #     (Q(sender=user) & Q(receiver=bestie)) |
    #     (Q(sender=bestie) & Q(receiver=user))
    # ).order_by('timestamp')

    messages = ChatMessage.objects.filter(
        Q(sender=user, receiver=bestie) | Q(sender=bestie, receiver=user)
    ).order_by('timestamp')


    return render(request, 'myapp/chat.html', {
        'user': user,
        'bestie': bestie,
        'messages': messages,
    })

'''

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import ChatMessage

User = get_user_model()

@login_required
def chat_view(request, username):
    bestie = get_object_or_404(User, username=username)
    user = request.user

    # Combine usernames alphabetically to create room_name
    room_name = '_'.join(sorted([user.username, bestie.username]))

    # Fetch chat messages between both users, ordered by timestamp ascending
    messages = ChatMessage.objects.filter(
        sender__in=[user, bestie],
        receiver__in=[user, bestie]
    ).order_by('timestamp')

    context = {
        'bestie': bestie,
        'user': user,
        'messages': messages,
        'room_name': room_name,
    }
    return render(request, 'myapp/chat.html', context)
