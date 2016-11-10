from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
from . import models

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^company/$', views.CompanyView.as_view(), name='company'),
    url(r'^technicians/$', views.TechnicianListView.as_view(), name='technicians'),
    url(r'^technicians/(?P<pk>\d+)/$', views.TechnicianDetailView.as_view(), name='technician'),
    url(r'^jobs/$', views.JobListView.as_view(), name='jobs'),
    url(r'^jobs/(?P<pk>\d+)/$', views.JobDetailView.as_view(), name='job'),
    url(r'^feedback/$', views.FeedbackListView.as_view(), name='feedbacks'),
    url(r'^feedback/(?P<pk>\d+)/$', views.FeedbackDetailView.as_view(), name='feedback'),
]
