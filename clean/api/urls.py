from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^jobs',
        views.JobCollection.as_view(),
        name='job_collection'),
    ]