from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from .forms import LoginForm
from django.contrib.auth import logout

class LoginView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm  # Usa el formulario personalizado
    redirect_authenticated_user = True  # Redirige usuarios autenticados


def salir(request):
    logout(request)
    return redirect('login')