from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^jobs', views.JobCollection.as_view(), name='job_collection'),
    url(r'^feedback/', views.FeedbackCollection.as_view(), name='feedback_collection'),
    url(r'^feedback-levels/', views.FeedbackLevelCollection.as_view(), name='feedback_level_collection'),
    url(r'^technicians/', views.TechnicianCollection.as_view(), name='technician_collection'),
]
