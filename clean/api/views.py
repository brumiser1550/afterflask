from rest_framework import generics
from rest_framework import filters
from .. import models
from . import serializers as my_serializers
from . import filters as my_filters
from . import metadata as my_metadata


class JobCollection(generics.ListAPIView):
    queryset = models.Job.objects.all()
    serializer_class = my_serializers.JobSerializer
    filter_class = my_filters.JobFilter
