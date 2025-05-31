# from django.contrib.sessions.models import Session
# from django.utils import timezone
# from django.contrib import messages
# from django.shortcuts import redirect
# from django.utils.deprecation import MiddlewareMixin

# class OneSessionPerUserMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         if request.user.is_authenticated:
#             current_session_key = request.session.session_key
#             user_sessions = Session.objects.filter(expire_date__gte=timezone.now())
#             # Flag to detect if current session is invalid
#             current_session_valid = False

#             for session in user_sessions:
#                 data = session.get_decoded()
#                 if data.get('_auth_user_id') == str(request.user.id):
#                     if session.session_key == current_session_key:
#                         current_session_valid = True
#                     else:
#                         # Delete other sessions (log them out)
#                         session.delete()

#             if not current_session_valid:
#                 # Current session has been invalidated (logged in elsewhere)
#                 from django.contrib.auth import logout
#                 logout(request)
#                 messages.info(request, "Your session was logged out")
#                 return redirect('login')


# yourapp/middleware.py
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout

class OneSessionPerUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            current_session_key = request.session.session_key
            user_sessions = Session.objects.filter(expire_date__gte=timezone.now())

            current_session_valid = False

            for session in user_sessions:
                data = session.get_decoded()
                if data.get('_auth_user_id') == str(request.user.id):
                    if session.session_key == current_session_key:
                        current_session_valid = True
                    else:
                        session.delete()

            if not current_session_valid:
                logout(request)
                return redirect('/login/?session_expired=1')  # Pass param
