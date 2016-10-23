from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Job)
admin.site.register(models.Technician)
admin.site.register(models.Contact)
admin.site.register(models.FeedbackLevel)
admin.site.register(models.Feedback)
