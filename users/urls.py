from django.urls import path, include

from . import views


app_name = "users"


urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),

    path('', include('django.contrib.auth.urls')),
]