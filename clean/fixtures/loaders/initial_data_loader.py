import os
import django
from django.conf import settings
django.setup()
from django.contrib.auth.models import User
from collections import namedtuple
from datetime import datetime
from clean import models

data_path = os.path.join(settings.BASE_DIR,
                         'clean/fixtures/data/initial_data.csv')

Row = namedtuple('Row', 'service_ceo_id feedback_comment tech_1 tech_2 tech_3 tech_4 job_id contact_id quality_inspector feedback_score quality_check_score job_scheduled quality_feedback_comment')

f = open(data_path, 'r')
data = [Row(*row.strip().split(',')) for row in f.readlines()
        if len(row.strip().split(',')) == 13]
f.close()

contacts = list(set([row.contact_id for row in data[1:]
            if row.job_id.isnumeric()
            and row.contact_id.isnumeric()]))

for contact in contacts:
    new_contact = models.Contact(contact_id=contact)
    new_contact.save()

jobs = [(int(row.job_id),
         datetime.strptime(row.job_scheduled, '%m/%d/%Y'),
         int(row.contact_id))
        for row in data[1:] if row.job_id.isnumeric()]

for job in jobs:
    contact = models.Contact.objects.filter(contact_id=job[2]).first()
    new_job = models.Job(job_id=job[0],
                         scheduled=job[1],
                         completed=job[1],
                         contact=contact)
    new_job.save()

techs =list(set([tech for row in data[1:]
                 for tech in [row.tech_1, row.tech_2, row.tech_3, row.tech_4]
                 if tech != '']))

counter = 0
for tech in techs:
    user = User.objects.create_user(tech, 'tech{}@tech.com'.format(counter))
    user.save()
    new_tech = models.Technician(name=tech, user=user, type='4').save()
    counter += 1

levels = {
    0: "No Rating",
    1: "Red",
    2: "Yellow",
    3: "Green",
    4: "Gold",
}

for level, title in levels.items():
    new_feedback_score = models.FeedbackLevel(value=int(level), title=title).save()

for row in data[1:]:
    if row.job_id.isnumeric():
        feedback_score = models.FeedbackLevel.objects.filter(value=row.feedback_score).first()
        job = models.Job.objects.filter(job_id=int(row.job_id)).first()
        new_feedback = models.Feedback(job=job,
                                       level=feedback_score,
                                       message=row.feedback_comment)
        new_feedback.save()
        job.company_feedback = new_feedback
        job.save()
        for tech in [row.tech_1, row.tech_2, row.tech_3, row.tech_4]:
            if tech != '':
                tech = models.Technician.objects.filter(name=tech).first()
                new_feedback = models.Feedback(job=job,
                                               tech=tech,
                                               level=feedback_score,
                                               message=row.feedback_comment).save()
