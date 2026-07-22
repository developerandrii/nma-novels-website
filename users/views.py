from django.views.generic import CreateView
from django.contrib.auth.forms import BaseUserCreationForm
from django.urls import reverse_lazy

class RegisterView(CreateView):
    form_class = BaseUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('users:login')

