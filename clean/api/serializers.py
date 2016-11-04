from datetime import datetime, timedelta
from django.db.models import Avg
from rest_framework import serializers
from .. import models


class ContactSerializer(serializers.ModelSerializer):
    """ This serializer is getting the data for a Contact. """

    class Meta:
        model = models.Contact
        fields = ('name_first', 'name_last', 'phone', 'address', 'email', 'contact_id')


class TechnicianSerializer(serializers.ModelSerializer):
    """ This serializer is getting the data for a Technician. """
    type_title = serializers.SerializerMethodField()
    weekly_scores = serializers.SerializerMethodField()

    class Meta:
        model = models.Technician
        fields = ('name', 'user', 'type', 'type_title', 'weekly_scores')

    def get_type_title(self, obj):
        return obj.get_type_display()

    def get_weekly_scores(self, obj):
        today = datetime.today()
        week1 = today - timedelta(days=7)
        week2 = today - timedelta(days=14)
        week3 = today - timedelta(days=21)
        week4 = today - timedelta(days=28)
        week1_score = models.Feedback.objects.filter(tech=obj,
                                                     level__value__gt=0,
                                                     job__completed__gt=week1,
                                                     job__completed__lt=today)
        week1_score = week1_score.aggregate(Avg('level__value'))['level__value__avg']
        week2_score = models.Feedback.objects.filter(tech=obj,
                                                     level__value__gt=0,
                                                     job__completed__gt=week2,
                                                     job__completed__lt=week1)
        week2_score = week2_score.aggregate(Avg('level__value'))['level__value__avg']
        week3_score = models.Feedback.objects.filter(tech=obj,
                                                     level__value__gt=0,
                                                     job__completed__gt=week3,
                                                     job__completed__lt=week2)
        week3_score = week3_score.aggregate(Avg('level__value'))['level__value__avg']
        week4_score = models.Feedback.objects.filter(tech=obj,
                                                     level__value__gt=0,
                                                     job__completed__gt=week4,
                                                     job__completed__lt=week3)
        week4_score = week4_score.aggregate(Avg('level__value'))['level__value__avg']
        return {'week1': week1_score,
                'week2': week2_score,
                'week3': week3_score,
                'week4': week4_score}


class FeedbackLevelSerializer(serializers.ModelSerializer):
    """ This serializer is getting the data for a Feedback Level. """

    class Meta:
        model = models.FeedbackLevel
        fields = ('title', 'value')


class CompanyFeedbackSerializer(serializers.ModelSerializer):
    """ This serializer is getting the data for a Feedback. """
    level = FeedbackLevelSerializer(read_only=True)
    tech = TechnicianSerializer(read_only=True)

    class Meta:
        model = models.Feedback
        fields = ('id', 'tech', 'level', 'message')


class JobSerializer(serializers.ModelSerializer):
    """ This serializer is getting the data for a Job. """
    contact = ContactSerializer(read_only=True)
    techs = TechnicianSerializer(read_only=True, many=True)
    company_feedback = CompanyFeedbackSerializer(read_only=True)

    class Meta:
        model = models.Job
        fields = ('scheduled', 'completed', 'id', 'job_id', 'contact', 'techs', 'company_feedback')

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


