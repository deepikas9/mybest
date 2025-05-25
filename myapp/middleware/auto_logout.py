import datetime
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = datetime.datetime.now()
            last_activity = request.session.get('last_activity')

            if last_activity:
                elapsed = (now - datetime.datetime.fromisoformat(last_activity)).total_seconds()
                if elapsed > settings.AUTO_LOGOUT_DELAY:
                    logout(request)
                    messages.info(request, 'You have been logged out due to inactivity.')
                    return redirect('login')  # Ensure this URL name exists

                    # Optional: add a message here or redirect
            request.session['last_activity'] = now.isoformat()

        response = self.get_response(request)
        return response
