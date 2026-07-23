from django.views.generic import CreateView, DetailView
from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse

from .models import User

class RegisterView(CreateView):
    form_class = BaseUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('users:login')


class CustomLoginView(LoginView):

    def get_success_url(self):
        return reverse('users:user-detail', kwargs={'pk': self.request.user.pk})




class UserDetailView(DetailView):
    model = User

