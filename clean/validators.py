"""
Borrowed from:
http://blog.jeremyaldrich.net/en/latest/django_filefield_csv_validation.html


"""

import csv
from datetime import datetime

from django.core.exceptions import ValidationError

import models

# used to map csv headers to location fields
# headers will be case insensitive
HEADERS = {'S1': {'email': {'field': 'email', 'required': True},
                  'jobid': {'field': 'jobid', 'required': True}
                  },
           'S2': {'CustomerID': {'field': 'CustomerID', 'required': True},
                  'Job': {'field': 'Job', 'required': True}
                  }
           }


def import_document_validator(document, file_type):
    # check file valid csv format
    if document.name.split('.')[-1] != 'csv':
        raise ValidationError(u'Not a valid CSV file')
    try:
        dialect = csv.Sniffer().sniff(document.read(1024))
        document.seek(0, 0)
    except csv.Error:
        raise ValidationError(u'Not a valid CSV file')
    reader = csv.reader(document.read().splitlines(), dialect)
    csv_headers = []
    required_headers = [header_name.lower() for header_name, values in
                        HEADERS[file_type].items() if values['required']]
    for y_index, row in enumerate(reader):
        # check that all headers are present
        if y_index == 0:
            # store header_names to sanity check required cells later
            csv_headers = [header_name.lower() for header_name in row if header_name]
            missing_headers = set(required_headers) - set([r.lower() for r in row])
            if missing_headers:
                missing_headers_str = ', '.join(missing_headers)
                raise ValidationError(u'Missing headers: %s' % (missing_headers_str))
            continue
        # ignore blank rows
        if not ''.join(str(x) for x in row):
            continue
        # sanity check required cell values
        for x_index, cell_value in enumerate(row):
            # if indexerror, probably an empty cell past the headers col count
            try:
                csv_headers[x_index]
            except IndexError:
                continue
            if csv_headers[x_index] in required_headers:
                if not cell_value:
                    raise ValidationError(u'Missing required value %s for row %s' %
                                            (csv_headers[x_index], y_index + 1))
    return True


def import_document_processor(document, file_type):
    reader = csv.DictReader(document)

    no_rating = models.FeedbackLevel.objects.filter(value=0).first()

    if file_type == 'S1':
        for row in reader:
            email = row['Email'].strip()
            name_first = row['First Name'].strip()
            name_last = row['Last Name'].strip()
            jobID = row['JobID'].strip()
            scheduled = datetime.strptime(row['CleaningAppointmentDate'].strip(),
                                          '%m/%d/%y')
            contact = models.Contact.objects.filter(email=email)
            if not contact.exists():
                contact = models.Contact.objects.create(name_first=name_first,
                                                        name_last=name_last,
                                                        email=email)
            else:
                # Should probably check to make sure that
                # we are not pulling more than one here
                contact = contact.first()
            job = models.Job.objects.filter(job_id=jobID)
            if not job.exists():
                job = models.Job.objects.create(job_id=jobID,
                                                contact=contact,
                                                scheduled=scheduled)
            else:
                # Should probably check to make sure that
                # we are not pulling more than one here
                job = job.first()
            # Create Company Feedback
            feedback = models.Feedback.objects.filter(job=job)
            if not feedback.exists():
                feedback = models.Feedback.objects.create(job=job,
                                                          level=no_rating
                                                          )
            else:
                # Should probably check to make sure that
                # we are not pulling more than one here
                feedback = feedback.first()
    else:
        for row in reader:
            email = row['email'].strip()
            jobID = row['Job'].strip()
            name_first = row['FirstName'].strip()
            name_last = row['LastName'].strip()
            techs = [row[col].strip()
                     for col in ['Custom 1', 'Custom 2', 'Custom 3', 'Employee4']
                     if row[col] != '']
            contact = models.Contact.objects.filter(email=email)
            if not contact.exists():
                contact = models.Contact.objects.create(name_first=name_first,
                                                        name_last=name_last,
                                                        email=email)
            else:
                # Should probably check to make sure that
                # we are not pulling more than one here
                contact = contact.first()
            job = models.Job.objects.filter(job_id=jobID)
            # There should be a job and we should only get one but we should
            # probably put code here to ensure that
            job = job.first()

            # Add completed time as now
            job.completed = datetime.now()
            job.save()

            for tech in techs:
                print(techs, tech)
                tech = models.Technician.objects.filter(name=tech)
                if not tech.exists():
                    print("TECH THAT DOESN'T EXIST")
                    continue
                else:
                    # Should probably check to make sure that
                    # we are not pulling more than one here
                    tech = tech.first()

                feedback = models.Feedback.objects.filter(job=job, tech=tech)
                if not feedback.exists():
                    feedback = models.Feedback.objects.create(job=job,
                                                              level=no_rating,
                                                              tech=tech
                                                              )
                else:
                    # Should probably check to make sure that
                    # we are not pulling more than one here
                    feedback = feedback.first()
    return True

