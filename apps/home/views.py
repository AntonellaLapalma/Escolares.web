from django.shortcuts import render, redirect
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name='index.html'

class InicioView(IndexView):
    template_name='inicio.html'
    
    def get(self,request):
        # En caso de que no se haya iniciado sesion redirige a login
        if not request.user.is_authenticated:
            return redirect('login')  
        
        return render (request, self.template_name)
        