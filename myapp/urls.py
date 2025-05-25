from django.urls import path
from .views import login_view, register_view, profile_view,forgot_password_view, home_view, besties_view, add_bestie_view, edit_profile
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name='login'),
    #path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('home/', home_view, name='home'),
    path('besties/', besties_view, name='besties'),
    path('add_bestie/', add_bestie_view, name='add_bestie'),
    path('settings/', edit_profile, name='settings'),
]
