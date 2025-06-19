# """
# ASGI config for ume project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
# """
# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ume.settings')
# import django
# django.setup()  # 🛠 Initialize the app registry

# # ✅ NOW it's safe to import other Django modules
# import myapp.routing

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             myapp.routing.websocket_urlpatterns
#         )
#     ),
# })
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ume.settings')

application = get_asgi_application()
