import os
import django
from django.conf import settings
django.setup()
from collections import namedtuple
from datetime import datetime
from clean import models

data_path = os.path.join(settings.BASE_DIR,
                         'clean/fixtures/data/initial_data.csv')

Row = namedtuple('Row', 'service_ceo_id feedback_comment tech_1 tech_2 tech_3 tech_4 job_id contact_id quality_inspector feedback_score quality_check_score job_scheduled quality_feedback_comment')

f = open(data_path, 'r')
data = [Row(*row.strip().split(',')) for row in f.readlines() if len(row.strip().split(',')) == 13]
f.close()

jobs = [(int(row.job_id), datetime.strptime(row.job_scheduled, '%m/%d/%Y'))
        for row in data[1:] if row.job_id.isnumeric()]

for job in jobs:
    new_job = models.Job(job_id=job[0], scheduled=job[1], completed=job[1])
    new_job.save()

