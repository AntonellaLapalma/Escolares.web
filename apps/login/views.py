from django.contrib.auth.views import LoginView
from .forms import LoginForm

class LoginView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm  # Usa el formulario personalizado
    redirect_authenticated_user = True  # Redirige usuarios autenticados
