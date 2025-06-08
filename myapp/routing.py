# # from django.urls import re_path
# # from . import consumers

# # websocket_urlpatterns = [
# #     re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
# # ]


# from django.urls import re_path
# from . import consumers

# websocket_urlpatterns = [
#     # For chat rooms or private chats, room_name can be the chat identifier (e.g. usernames combined)
#     re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),

#     # Keep notification consumer if you have one
#     #re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
# ]



from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # WebSocket route for private 1-on-1 chat
    #re_path(r'^ws/chat/(?P<room_name>[a-zA-Z0-9_]+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>[\w.@+-]+)/$', consumers.ChatConsumer.as_asgi()),

]
