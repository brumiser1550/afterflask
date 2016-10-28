from rest_framework import serializers
from .. import models


class JobSerializer(serializers.ModelSerializer):
    """ This serializer is getting the data for a Job. """

    class Meta:
        model = models.Job
        fields = ('scheduled', 'completed', 'id')