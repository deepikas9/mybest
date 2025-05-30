from django.urls import path
from .views import login_view, register_view, profile_view,forgot_password_view, home_view, besties_view, add_bestie_view, edit_profile
from django.contrib.auth.views import LogoutView
from .views import search_bestie,add_bestie, bestie_list, remove_bestie,bestie_inbox,accept_bestie

urlpatterns = [
    path('login/', login_view, name='login'),
    #path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('home/', bestie_inbox, name='home'),
    path('besties/', besties_view, name='besties'),
    path('add_bestie/', add_bestie_view, name='add_bestie'),
    path('settings/', edit_profile, name='settings'),
    path('search-bestie/', search_bestie, name='search_bestie'),
    path('add-bestie/<int:user_id>/', add_bestie, name='add_bestie'),
    path('my-besties/', bestie_list, name='bestie_list'),
    path('accept-bestie/<int:user_id>/', accept_bestie, name='accept_bestie'),
    path('remove-bestie/<int:user_id>/', remove_bestie, name='remove_bestie'),

    
]
