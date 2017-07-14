from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import FormView


class SignUpView(FormView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'authentication/signup.html'

    def form_valid(self, form):
        User = get_user_model()
        User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        return super().form_valid(form)
