from django.db import models
from django.contrib.auth.models import User


class Technician(models.Model):
    name = models.CharField(max_length=60)
    user = models.ForeignKey(User)

    def __str__(self):
        return "Tech: {} email: {}".format(self.name, self.user.email)


class Contact(models.Model):
    name_first = models.CharField(max_length=60, null=True, blank=True)
    name_last = models.CharField(max_length=60, null=True, blank=True )
    phone = models.CharField(max_length=12, null=True, blank=True)
    address = models.TextField(max_length=240, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    contact_id = models.IntegerField()

    def __str__(self):
        return "Contact: {} {} - email: {}".format(self.name_first, self.name_last, self.user.email)


class Job(models.Model):
    scheduled = models.DateTimeField()
    completed = models.DateTimeField()
    job_id = models.IntegerField()
    contact = models.ForeignKey(Contact, null=True)

    def __str__(self):
        return "Job {} - job_id: {} Scheduled: {}  Completed: {}".format(self.pk, self.job_id, self.scheduled, self.completed)


class FeedbackLevel(models.Model):
    title = models.CharField(max_length=140)
    value = models.IntegerField()

    def __str__(self):
        return "Level: {} - Value {}".format(self.title, self.value)


class Feedback(models.Model):
    job = models.ForeignKey(Job)
    tech = models.ForeignKey(Technician)
    level = models.ForeignKey(FeedbackLevel)
    message = models.TextField(blank=True)

    def __str__(self):
        return "Feedback - Job {} - {} - {}".format(self.job.job_id, self.tech.name, self.level.title)