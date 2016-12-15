from rest_framework import generics
from rest_framework import filters
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .. import models
from . import serializers as my_serializers
from . import filters as my_filters
from . import metadata as my_metadata
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer


class JobCollection(generics.ListAPIView):
    # queryset = models.Job.objects.all()
    model = models.Job
    serializer_class = my_serializers.JobSerializer
    filter_class = my_filters.JobFilter
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
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


class CustomFeedbackPost(APIView):
    # parser_classes = (FormParser, MultiPartParser,)

    def get(self, request, format=None):
        return Response({"success": True, "content": "Hello World!"})

    def post(self, request, format=None):
        levels = {
            0: "No Rating",
            1: "Red",
            2: "Yellow",
            3: "Green",
            4: "Gold",
        }
        contact_id = request.data.get('contact_id', None)
        name_first = request.data.get('name_first', None)
        name_last = request.data.get('name_last', None)
        email = request.data.get('email', None)
        phone = request.data.get('phone', None)
        address = request.data.get('address', None)
        job_id = request.data.get('job_id', None)
        scheduled = request.data.get('scheduled', None)
        if not scheduled:
            scheduled = datetime.today()
        else:
            scheduled = datetime.strptime(scheduled, '%m/%d/%Y')
        level = int(request.data.get('level', 0))
        title = levels[level]
        feedback_score = models.FeedbackLevel.objects.filter(value=level).first()
        message = request.data.get('message', None)
        tech1 = request.data.get('tech1', None)
        tech2 = request.data.get('tech2', None)
        tech3 = request.data.get('tech3', None)
        tech4 = request.data.get('tech4', None)

        if not contact_id or not job_id:
            return Response("Missing required parameters")

        contact = models.Contact.objects.filter(contact_id=contact_id).first()
        if not contact:
            contact = models.Contact(contact_id=contact_id)
        contact.name_first = name_first
        contact.name_last = name_last
        contact.email = email
        contact.phone = phone
        contact.address = address
        contact.save()

        job = models.Job(job_id=job_id,
                         scheduled=scheduled,
                         completed=scheduled,
                         contact=contact)
        job.save()

        new_feedback = models.Feedback(job=job,
                                       level=feedback_score,
                                       message=message)
        new_feedback.save()

        job.company_feedback = new_feedback
        job.save()

        for tech_name in [tech1, tech2, tech3, tech4]:
            if tech_name and len(tech_name) > 3:
                tech = models.Technician.objects.filter(name=tech_name).first()
                if not tech:
                    user = User.objects.filter(username=tech_name).first()
                    if not user:
                        user = User.objects.create_user(tech_name, '{}@naturalccs.com'.format(tech_name.replace(" ", ".")))
                        user.save()
                    tech = models.Technician(name=tech_name, user=user, type='4')
                    tech.save()
                new_feedback = models.Feedback(job=job,
                                               tech=tech,
                                               level=feedback_score,
                                               message=message).save()

        return Response({"success": True})
