from django.urls import path
from .views import (
    login_view, register_view, forgot_password_view, home_view,
    add_bestie_view, edit_profile, chat_view, logout_view,get_reaction_counts, toggle_reaction,get_reactions,
    search_bestie, add_bestie, bestie_list, remove_bestie,chat_status,typing_status_view, delete_chat, react_to_post,emoji_reaction,
    bestie_inbox, accept_bestie, cancel_bestie_request,get_messages, send_message,unread_counts_view, trendz, edit_post, delete_post
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('home/', home_view, name='home'),
    path('settings/', edit_profile, name='settings'),
    path('trendz/', trendz, name='trendz'),
    path('trendz/edit/<int:post_id>/', edit_post, name='edit_post'),
    path('trendz/delete/<int:post_id>/', delete_post, name='delete_post'),
    #path('react/', react_to_post, name='react_to_post'),
    path("emoji_reaction/", emoji_reaction, name="emoji_reaction"),
    # Bestie logic
    path('add_bestie/', add_bestie_view, name='add_bestie_view'),
    path('add-bestie/<int:user_id>/', add_bestie, name='add_bestie'),
    path('search-bestie/', search_bestie, name='search_bestie'),
    path('my-besties/', bestie_list, name='bestie_list'),
    path('accept-bestie/<int:user_id>/', accept_bestie, name='accept_bestie'),
    path('remove-bestie/<int:user_id>/', remove_bestie, name='remove_bestie'),
    path('cancel-bestie/<int:user_id>/', cancel_bestie_request, name='cancel_bestie_request'),
    # urls.py
    path('reactions/<int:post_id>/', get_reaction_counts, name='get_reaction_counts'),
    path("react/<int:post_id>/", toggle_reaction, name="toggle_reaction"),
    path("get-reactions/", get_reactions, name="get_reactions"),
    



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
