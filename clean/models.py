from django.db import models
from django.contrib.auth.models import User


class Technician(models.Model):
    TYPES = (
        ('1', 'Office Staff'),
        ('2', 'Quality Checker'),
        ('3', 'Admin'),
        ('4', 'Operations'),
    )

    name = models.CharField(max_length=60)
    user = models.ForeignKey(User)
    type = models.CharField(max_length=2, choices=TYPES)

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
        return "Contact: {} {} - email: {}".format(self.name_first, self.name_last, self.email)


class Job(models.Model):
    scheduled = models.DateTimeField()
    completed = models.DateTimeField()
    job_id = models.IntegerField()
    contact = models.ForeignKey(Contact, null=True)
    company_feedback = models.ForeignKey('Feedback', blank=True, null=True, related_name='job_feedback')

    def __str__(self):
        return "Job {} - job_id: {} Scheduled: {}  Completed: {}".format(self.pk, self.job_id, self.scheduled, self.completed)

    @property
    def techs(self):
        return [feedback.tech for feedback in self.feedback_set.all() if feedback.tech is not None]


class FeedbackLevel(models.Model):
    title = models.CharField(max_length=140)
    value = models.IntegerField()

    def __str__(self):
        return "Level: {} - Value {}".format(self.title, self.value)


class Feedback(models.Model):
    job = models.ForeignKey(Job)
    level = models.ForeignKey(FeedbackLevel)
    message = models.TextField(blank=True)
    tech = models.ForeignKey(Technician, null=True, blank=True)

    def __str__(self):
        return "Feedback - Job {} - {}".format(self.job.job_id, self.level.title)


class Acknowledgement(models.Model):
    feedback = models.ForeignKey(Feedback)
    message = models.TextField(blank=True)


class UploadedData(models.Model):
    """ UploadedData Model

    """
    FILE_TYPES = (('S1', 'Sheet 1'),
                  ('S2', 'Sheet 2'))
    uploaded_by = models.ForeignKey(User)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    data = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)

    def __str__(self):
        return "{} - Uploaded By: {} - Uploaded On: {}".format(self.file_type,
                                                               self.uploaded_by,
                                                               self.uploaded_on)