from django.urls import path
from .views import (
    login_view, register_view, forgot_password_view, home_view,
    add_bestie_view, edit_profile, chat_view, logout_view,
    search_bestie, add_bestie, bestie_list, remove_bestie,chat_status,typing_status_view, delete_chat,
    bestie_inbox, accept_bestie, cancel_bestie_request,get_messages, send_message,unread_counts_view
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('home/', home_view, name='home'),
    path('settings/', edit_profile, name='settings'),

    # Bestie logic
    path('add_bestie/', add_bestie_view, name='add_bestie_view'),
    path('add-bestie/<int:user_id>/', add_bestie, name='add_bestie'),
    path('search-bestie/', search_bestie, name='search_bestie'),
    path('my-besties/', bestie_list, name='bestie_list'),
    path('accept-bestie/<int:user_id>/', accept_bestie, name='accept_bestie'),
    path('remove-bestie/<int:user_id>/', remove_bestie, name='remove_bestie'),
    path('cancel-bestie/<int:user_id>/', cancel_bestie_request, name='cancel_bestie_request'),

    # Chat
    #path('chat/<str:username>/', chat_view, name='chat'),
    path('chat/<str:username>/', chat_view, name='chat'),
    path('chat/get_messages/<int:receiver_id>/', get_messages, name='get_messages'),
    path('chat/send_message/<int:receiver_id>/', send_message, name='send_message'),
    path('ajax/unread-counts/', unread_counts_view, name='unread_counts'),

    #MII
    #path('mii/', MiiAssistantView.as_view(), name='mii-assistant'),
    path('chat/chat_status/<int:bestie_id>/', chat_status, name='chat_status'),
    path('chat/typing-status/<int:bestie_id>/', typing_status_view, name='typing_status'),

    path('chat/delete_chat/<int:user_id>/', delete_chat, name='delete_chat'),


]
