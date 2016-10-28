from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    scheduled = models.DateTimeField()
    completed = models.DateTimeField()
    job_id = models.IntegerField()


class Technician(models.Model):
    name = models.CharField(max_length=60)
    user = models.ForeignKey(User)


class Contact(models.Model):
    name_first = models.CharField(max_length=60)
    name_last = models.CharField(max_length=60)
    phone = models.CharField(max_length=12)
    address = models.TextField(max_length=240)
    email = models.EmailField()


class FeedbackLevel(models.Model):
    title = models.CharField(max_length=140)
    value = models.IntegerField()


class Feedback(models.Model):
    job = models.ForeignKey(Job)
    tech = models.ForeignKey(Technician)
    level = models.ForeignKey(FeedbackLevel)