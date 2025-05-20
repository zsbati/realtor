from django.db import migrations
from django.utils import timezone

def update_timezones(apps, schema_editor):
    Visit = apps.get_model('agenda', 'Visit')
    for visit in Visit.objects.all():
        if visit.scheduled_date and timezone.is_naive(visit.scheduled_date):
            visit.scheduled_date = timezone.make_aware(visit.scheduled_date)
            visit.save(update_fields=['scheduled_date'])

class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(update_timezones, migrations.RunPython.noop),
    ]
