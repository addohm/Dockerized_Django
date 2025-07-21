from django.urls import path
from . import views  # Import views from the current directory

urlpatterns = [
    path("", views.basic_view, name="hello_world"),
]