from django.views import generic
from django.shortcuts import get_object_or_404
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(generic.TemplateView):
    template_name = "clean/home.html"


class TechnicianListView(LoginRequiredMixin, generic.TemplateView):
    model = models.Technician
    template_name = "clean/technicians_list.html"

    def get_context_data(self, **kwargs):
        context = super(TechnicianListView, self).get_context_data(**kwargs)
        return context


class TechnicianDetailView(LoginRequiredMixin, generic.TemplateView):
    model = models.Technician
    template_name = "clean/technicians_detail.html"

    def get_context_data(self, **kwargs):
        context = super(TechnicianDetailView, self).get_context_data(**kwargs)
        return context


class JobListView(LoginRequiredMixin, generic.TemplateView):
    model = models.Job
    template_name = "clean/jobs_list.html"

    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        return context


class JobDetailView(LoginRequiredMixin, generic.TemplateView):
    model = models.Job
    template_name = "clean/jobs_detail.html"

    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        return context


class FeedbackListView(LoginRequiredMixin, generic.TemplateView):
    model = models.Feedback
    template_name = "clean/feedback_list.html"

    def get_context_data(self, **kwargs):
        context = super(FeedbackListView, self).get_context_data(**kwargs)
        return context


class FeedbackDetailView(LoginRequiredMixin, generic.TemplateView):
    model = models.Feedback
    template_name = "clean/feedback_detail.html"

    def get_context_data(self, **kwargs):
        context = super(FeedbackDetailView, self).get_context_data(**kwargs)
        return context
