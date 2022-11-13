# Generated by Django 3.2 on 2021-11-16 08:00

from django.db import migrations, utils, transaction
from juntagrico.config import Config


def lowercase_emails(apps, schema_editor):
    Member = apps.get_model('juntagrico', 'Member')
    for member in Member.objects.all():
        member.email = member.email.lower()
        try:
            with transaction.atomic():
                member.save()
        except utils.IntegrityError:
            print('\nWARNING: Duplicate email address must be fixed manually: ', member.email)


def migrate_location(apps, schema_editor):
    JobType = apps.get_model('juntagrico', 'JobType')
    OneTimeJob = apps.get_model('juntagrico', 'OneTimeJob')
    Depot = apps.get_model('juntagrico', 'Depot')
    Location = apps.get_model('juntagrico', 'Location')
    for job_type in JobType.objects.all():
        job_type.location2 = Location.objects.get_or_create(name=job_type.location)[0]
        job_type.save()
    for one_time_job in OneTimeJob.objects.all():
        one_time_job.location2 = Location.objects.get_or_create(name=one_time_job.location)[0]
        one_time_job.save()
    for a_depot in Depot.objects.all():
        a_depot.location2 = Location.objects.get_or_create(
            name=f"{Config.vocabulary('depot')} {a_depot.name}",
            latitude=a_depot.latitude,
            longitude=a_depot.longitude,
            addr_street=a_depot.addr_street,
            addr_zipcode=a_depot.addr_zipcode,
            addr_location=a_depot.addr_location
        )[0]
        a_depot.save()


def migrate_contacts(apps, schema_editor):
    ActivityArea = apps.get_model('juntagrico', 'ActivityArea')
    TextContact = apps.get_model('juntagrico', 'TextContact')
    EmailContact = apps.get_model('juntagrico', 'EmailContact')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    for area in ActivityArea.objects.all():
        # if previous contact was not just name and email of coordinator, create contacts to display info as before
        if area.email:
            # In migration world everything must be done manually. The fake historic models won't do it
            area_ct = ContentType.objects.get_for_model(ActivityArea)
            text_ct = ContentType.objects.get_for_model(TextContact)
            email_ct = ContentType.objects.get_for_model(EmailContact)
            TextContact.objects.create(text=f'{area.coordinator.first_name} {area.coordinator.last_name}',
                                       polymorphic_ctype=text_ct,
                                       object_id=area.id, content_type=area_ct)
            EmailContact.objects.create(email=area.email,
                                        polymorphic_ctype=email_ct,
                                        object_id=area.id, content_type=area_ct)


class Migration(migrations.Migration):

    dependencies = [
        ('juntagrico', '0035_pre_1_5'),
    ]

    operations = [
        migrations.RunPython(migrate_location),
        migrations.RunPython(migrate_contacts),
        migrations.RunPython(lowercase_emails),
    ]