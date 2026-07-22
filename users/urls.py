from django.urls import path, include

from . import views


app_name = "users"


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
]