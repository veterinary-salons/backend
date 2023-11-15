from django.db import migrations, models

def check_if_field_exists(apps, schema_editor):
    schedule = apps.get_model('core', 'Schedule')
    if 'arround_clocks' in [f.name for f in schedule._meta.fields]:
        migrations.RenameField(
            model_name='yourmodel',
            old_name='arround_clocks',
            new_name='arround_clock',
        )

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_schedule_arround_clock'),
    ]

    operations = [
        migrations.RunPython(check_if_field_exists, reverse_code=migrations.RunPython.noop),
    ]
