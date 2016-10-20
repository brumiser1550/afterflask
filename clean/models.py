from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    scheduled = models.DateTimeField()
    completed = models.DateTimeField()


class Technician(models.Model):
    name = models.CharField(max_length=60)
    user = models.ForeignKey(User)


class Contact(models.Model):
    name_first = models.CharField(max_length=60)
    name_last = models.CharField(max_length=60)
    phone = models.CharField(max_length=12)
    address = models.TextField(max_length=240)
    email = models.EmailField()


class Feedback(models.Model):
    job = models.ForeignKey(Job)
    tech = models.ForeignKey(Technician)


# Questions
# 1 - Feedback has a FK to Rating.  There is no Rating on the paper.  Should this be feedback level?
# Are these just choices for feedback?  Do they need to be a table or can they
# be choices hard coded into the model/field?
# 2 - what are the permissions/permission levels for?  Is this meant to control
# who can see something or who can edit something?  If so we might use the django
# permission system?
# 3 - What is the JobID on Job?  How is it different from the regular ID?  is this
# just like a job name entered by the company or does it need to be some other kind of ID system?