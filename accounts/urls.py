from django.urls import path
from .views import signup_view,login_view,dashboard_view,logout_view,profile_setup_view

urlpatterns= [
    path('signup/',signup_view,name="signup"),
    path('login/',login_view,name="login"),
    path('logout',logout_view,name='logout'),
    path('dashboard/',dashboard_view,name="dashboard"),
    path('profile-setup/', profile_setup_view, name='profile-setup')
]