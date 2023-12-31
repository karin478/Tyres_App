# Generated by Django 4.2.5 on 2023-09-17 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tyres_App', '0003_sessionreturn_tyre_type_delete_tyresetreturn'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeekendTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('total_sets', models.IntegerField()),
                ('hard_sets', models.IntegerField()),
                ('medium_sets', models.IntegerField()),
                ('soft_sets', models.IntegerField()),
                ('sessions', models.JSONField()),
            ],
        ),
        migrations.RemoveField(
            model_name='tyresetusage',
            name='tyre_set',
        ),
        migrations.RemoveField(
            model_name='tyresetusage',
            name='weekend_session',
        ),
        migrations.RemoveField(
            model_name='tyreset',
            name='used_in_sessions',
        ),
        migrations.AddField(
            model_name='raceweekend',
            name='cars',
            field=models.ManyToManyField(related_name='race_weekends', to='Tyres_App.car'),
        ),
        migrations.AddField(
            model_name='weekendsession',
            name='sets_to_return_hard',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='weekendsession',
            name='sets_to_return_medium',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='weekendsession',
            name='sets_to_return_soft',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tyreset',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='SessionReturn',
        ),
        migrations.DeleteModel(
            name='TyreSetUsage',
        ),
    ]
