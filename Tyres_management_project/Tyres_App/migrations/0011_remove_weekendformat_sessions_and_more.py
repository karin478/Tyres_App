# Generated by Django 4.2.5 on 2023-09-17 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tyres_App', '0010_weekendsession_weekend_format'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weekendformat',
            name='sessions',
        ),
        migrations.AlterField(
            model_name='weekendsession',
            name='weekend_format',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='weekend_sessions', to='Tyres_App.weekendformat'),
            preserve_default=False,
        ),
    ]
