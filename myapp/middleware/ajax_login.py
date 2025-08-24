# myapp/middleware/ajax_login.py

from django.http import JsonResponse
from django.conf import settings

class AjaxLoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 302 and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            login_url = settings.LOGIN_URL
            if login_url in response.get('Location', ''):
                return JsonResponse({'error': 'Session expired'}, status=401)
        return response
