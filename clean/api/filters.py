import django_filters
from .. import models


class IntegerListFilter(django_filters.Filter):
    def filter(self, qs, value):
        if value not in (None, ''):
            integers = [int(v) for v in value.split(',')]
            return qs.filter(**{'{}__{}'.format(self.name, self.lookup_type): integers})
        return qs


class JobFilter(django_filters.FilterSet):
    id = IntegerListFilter(name='pk', lookup_type='in')

    class Meta:
        model = models.Job
        fields = ['scheduled', 'completed', 'job_id']


class FeedbackFilter(django_filters.FilterSet):
    id = IntegerListFilter(name='pk', lookup_type='in')

    class Meta:
        model = models.Feedback
        fields = ['job', 'techs', 'level', 'message']


class FeedbackLevelFilter(django_filters.FilterSet):
    id = IntegerListFilter(name='pk', lookup_type='in')

    class Meta:
        model = models.FeedbackLevel
        fields = ['title', 'value']
