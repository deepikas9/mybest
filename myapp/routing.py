# from django.urls import re_path
# from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
# ]


from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # For chat rooms or private chats, room_name can be the chat identifier (e.g. usernames combined)
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),

    # Keep notification consumer if you have one
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]
