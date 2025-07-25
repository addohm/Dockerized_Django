from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import IndexView, ContactFormCreateView, SentView, ProtectedView, CustomLoginView, ProfileUpdateView, ProfileDetailView


appname = "mainapp"

urlpatterns = [
    # Use if you want to break out your login redirect, correlates with settings.py LOGIN_URL
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile-update'),
    path('', IndexView.as_view(), name='index'),
    path('contact/', ContactFormCreateView.as_view(), name='contact'),
    path('sent/', SentView.as_view(), name='sent'),
]
