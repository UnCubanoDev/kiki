from django.db import migrations

def create_days_of_week(apps, schema_editor):
    DayOfWeek = apps.get_model('api', 'DayOfWeek')
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in days:
        DayOfWeek.objects.get_or_create(name=day)

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),  # Asegúrate de que esta sea la migración inicial
    ]

    operations = [
        migrations.RunPython(create_days_of_week),
    ] 