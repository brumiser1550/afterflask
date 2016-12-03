from rest_framework import generics
from rest_framework import filters
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .. import models
from . import serializers as my_serializers
from . import filters as my_filters
from . import metadata as my_metadata


class JobCollection(generics.ListAPIView):
    # queryset = models.Job.objects.all()
    model = models.Job
    serializer_class = my_serializers.JobSerializer
    filter_class = my_filters.JobFilter
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('completed',)
    ordering = ('-completed',)

    def get_queryset(self):
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        if not date_from or not date_to:
            return models.Job.objects.all()
        return models.Job.objects.filter(completed__gte=date_from,
                                         completed__lte=date_to)


class FeedbackCollection(generics.ListAPIView, ):
    queryset = models.Feedback.objects.all()
    serializer_class = my_serializers.FeedbackSerializer
    filter_class = my_filters.FeedbackFilter


class FeedbackDetail(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     generics.GenericAPIView):
    serializer_class = my_serializers.FeedbackSerializer
    filter_class = my_filters.FeedbackFilter

    def get_queryset(self):
        user = self.kwargs['pk']
        return models.Feedback.objects.filter(tech__user=user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class FeedbackLevelCollection(generics.ListAPIView):
    queryset = models.FeedbackLevel.objects.all()
    serializer_class = my_serializers.FeedbackLevelSerializer
    filter_class = my_filters.FeedbackLevelFilter


class TechnicianCollection(generics.ListAPIView):
    queryset = models.Technician.objects.all()
    serializer_class = my_serializers.TechnicianSerializer
    filter_class = my_filters.TechnicianFilter


class TechnicianDetail(generics.RetrieveAPIView):
    serializer_class = my_serializers.TechnicianSerializer
    filter_class = my_filters.TechnicianFilter

    def get_queryset(self):
        user = self.kwargs['pk']
        return models.Technician.objects.filter(user=user)


class UploadedDataCollection(generics.ListAPIView,
                             mixins.CreateModelMixin):
    queryset = models.UploadedData.objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = my_serializers.UploadedDataSerializer
    filter_class = my_filters.UploadedDataFilter

    def get_serializer_class(self):
        """This method provides the appropriate serializer."""
        if self.request.method == 'POST':
            return my_serializers.UploadedDataPostSerializer
        return self.serializer_class

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
