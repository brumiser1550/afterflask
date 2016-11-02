from rest_framework import serializers
from .. import models


class ContactSerializer(serializers.ModelSerializer):
    """ This serializer is getting the data for a Contact. """

    class Meta:
        model = models.Contact
        fields = ('name_first', 'name_last', 'phone', 'address', 'email', 'contact_id')


class TechnicianSerializer(serializers.ModelSerializer):
    """ This serializer is getting the data for a Contact. """

    class Meta:
        model = models.Technician
        fields = ('name', 'user', 'type')


class FeedbackLevelSerializer(serializers.ModelSerializer):
    """ This serializer is getting the data for a Feedback Level. """

    class Meta:
        model = models.FeedbackLevel
        fields = ('title', 'value')


class JobSerializer(serializers.ModelSerializer):
    """ This serializer is getting the data for a Job. """
    contact = ContactSerializer(read_only=True)
    techs = TechnicianSerializer(read_only=True, many=True)

    class Meta:
        model = models.Job
        fields = ('scheduled', 'completed', 'id', 'job_id', 'contact', 'techs')

    def get_contact(self, obj):
        return obj

    def get_techs(self, obj):
        return obj.techs


class FeedbackSerializer(serializers.ModelSerializer):
    """ This serializer is getting the data for a Feedback. """
    level = FeedbackLevelSerializer(read_only=True)
    job = JobSerializer(read_only=True)
    tech = TechnicianSerializer(read_only=True)

    class Meta:
        model = models.Feedback
        fields = ('id', 'job', 'tech', 'level', 'message')


