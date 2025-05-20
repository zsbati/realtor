from django.db import migrations
from django.utils import timezone

def update_timezones_final(apps, schema_editor):
    Visit = apps.get_model('agenda', 'Visit')
    for visit in Visit.objects.all():
        # This will trigger the property setter to ensure timezone awareness
        if visit.scheduled_date and timezone.is_naive(visit.scheduled_date):
            visit.scheduled_date = timezone.make_aware(visit.scheduled_date)
            visit.save(update_fields=['scheduled_date'])

class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0008_merge_20250520_2158'),
    ]

    operations = [
        migrations.RunPython(update_timezones_final, migrations.RunPython.noop),
    ]
