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
        fields = {
            'scheduled': ['contains'],
            'completed': ['date'],
            'job_id': ['exact'],
            'contact__name_first': ['contains'],
            'contact__name_last': ['contains'],
            'contact__contact_id': ['exact'],
        }


class FeedbackFilter(django_filters.FilterSet):
    id = IntegerListFilter(name='pk', lookup_type='in')

    class Meta:
        model = models.Feedback
        fields = ['job', 'tech', 'level', 'message']


class FeedbackLevelFilter(django_filters.FilterSet):
    id = IntegerListFilter(name='pk', lookup_type='in')

    class Meta:
        model = models.FeedbackLevel
        fields = ['title', 'value']


class TechnicianFilter(django_filters.FilterSet):
    id = IntegerListFilter(name='pk', lookup_type='in')

    class Meta:
        model = models.Technician
        fields = ['name', 'type']


class UploadedDataFilter(django_filters.FilterSet):
    id = IntegerListFilter(name='id', lookup_type='in')

    class Meta:
        model = models.UploadedData
        fields = ['id', 'uploaded_by', 'uploaded_on', 'file_type']
