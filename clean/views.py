from django.views import generic
from django.shortcuts import get_object_or_404
from . import models


class MainView(generic.TemplateView):
    template_name = "clean/home.html"