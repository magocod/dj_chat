from django.shortcuts import render

#vista genericas
from django.views.generic import TemplateView

# Create your views here.

#vista pantalla de inicio aplicacion 
class Indexv1(TemplateView):
	#plantilla
    template_name = "index.html"