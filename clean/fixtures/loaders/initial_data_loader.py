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

jobs = [(int(row.job_id), datetime.strptime(row.job_scheduled, '%m/%d/%Y'))
        for row in data[1:] if row.job_id.isnumeric()]

for job in jobs:
    new_job = models.Job(job_id=job[0], scheduled=job[1], completed=job[1])
    new_job.save()

techs =list(set([tech for row in data[1:]
                 for tech in [row.tech_1, row.tech_2, row.tech_3, row.tech_4]
                 if tech != '']))

counter = 0
for tech in techs:
    user = User.objects.create_user(tech, 'tech{}@tech.com'.format(counter))
    user.save()
    new_tech = models.Technician(name=tech, user=user).save()
    counter += 1

levels = list(set([row.feedback_score for row in data[1:]]))

for level in levels:
    new_feedback_score = models.FeedbackLevel(value=int(level), title=level).save()

for row in data[1:]:
    if row.job_id.isnumeric():
        feedback_score = models.FeedbackLevel.objects.filter(title=row.feedback_score).first()
        job = models.Job.objects.filter(job_id=int(row.job_id)).first()
        for tech in [row.tech_1, row.tech_2, row.tech_3, row.tech_4]:
            if tech != '':
                tech = models.Technician.objects.filter(name=tech).first()
                new_feedback = models.Feedback(job=job,
                                               tech=tech,
                                               level=feedback_score).save()
