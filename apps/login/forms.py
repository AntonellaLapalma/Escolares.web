from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validar_num(value):
    if not value.isdigit():
        raise ValidationError('Por favor, ingrese solo números.')
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=10,
        required=True,
        validators=[validar_num],
        widget=forms.TextInput(attrs={'placeholder': ''}))
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': ''}))
    
    class Meta:
        #indica que esta relacionado con el modelo de usuario de django haciendo uso de estos dos campos
        model = User
        fields = ('username', 'password')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError('El usuario no existe.')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError('')
        
        if not user.check_password(password):
            raise ValidationError('La contraseña es incorrecta.')
        return password


    






