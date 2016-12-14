from datetime import datetime, timedelta
from django.db.models import Avg, Count
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
    feedback_totals = serializers.SerializerMethodField()
    all_time_gold = serializers.SerializerMethodField()

    class Meta:
        model = models.Technician
        fields = ('name', 'user', 'type', 'type_title',
                  'weekly_scores', 'feedback_totals', 'all_time_gold')

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

    def get_feedback_totals(self, obj):
        tech_feedback = models.Feedback.objects.filter(tech=obj)
        feedback = tech_feedback.values("tech",
                                        "level__title",
                                        "level__value").annotate(Count("level__value")).order_by()
        return [{'title': x['level__title'],
                 'total': x['level__value__count'],
                 'value': x['level__value'],
                 } for x in feedback]

    def get_all_time_gold(self, obj):
        # What should the result be if null, 0?  Same issue in week scores.
        score = models.Feedback.objects.filter(tech=obj,
                                               level__value__gt=0)
        score = score.aggregate(Avg('level__value'))['level__value__avg']
        return score


class FeedbackLevelSerializer(serializers.ModelSerializer):
    """ This serializer is getting the data for a Feedback Level. """
    count = serializers.SerializerMethodField()

    class Meta:
        model = models.FeedbackLevel
        fields = ('title', 'value', 'count')

    def get_count(self, obj):
        request = self.context['request']
        date_from = request.query_params.get('date_from', None)
        date_to = request.query_params.get('date_to', None)
        if not date_from or not date_to:
            count = models.Feedback.objects.filter(level__value=obj.value).count()
            return count
        count = models.Feedback.objects.filter(level__value=obj.value,
                                               job__completed__gte=date_from,
                                               job__completed__lte=date_to).count()
        return count


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


class UploadedDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UploadedData
        fields = ('id', 'uploaded_by', 'uploaded_on', 'data', 'file_type')


class UploadedDataPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UploadedData
        fields = ('id', 'data', 'file_type')
