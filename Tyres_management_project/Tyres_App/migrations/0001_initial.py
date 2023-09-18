# Generated by Django 4.2.5 on 2023-09-16 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RaceWeekend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='TyreSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Soft', 'Soft'), ('Medium', 'Medium'), ('Hard', 'Hard')], max_length=10)),
                ('state', models.CharField(choices=[('New', 'New'), ('Used', 'Used')], max_length=10)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tyre_sets', to='Tyres_App.car')),
            ],
        ),
        migrations.CreateModel(
            name='WeekendSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('is_race_session', models.BooleanField(default=False)),
                ('race_weekend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='Tyres_App.raceweekend')),
            ],
        ),
        migrations.CreateModel(
            name='WeekendFormat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('total_sets', models.IntegerField()),
                ('hard_sets', models.IntegerField()),
                ('medium_sets', models.IntegerField()),
                ('soft_sets', models.IntegerField()),
                ('sessions', models.ManyToManyField(related_name='weekend_formats', to='Tyres_App.weekendsession')),
            ],
        ),
        migrations.CreateModel(
            name='TyreSetUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('tyre_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usages', to='Tyres_App.tyreset')),
                ('weekend_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tyre_set_usages', to='Tyres_App.weekendsession')),
            ],
        ),
        migrations.CreateModel(
            name='TyreSetReturn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('tyre_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='returns', to='Tyres_App.tyreset')),
                ('weekend_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tyre_set_returns', to='Tyres_App.weekendsession')),
            ],
        ),
        migrations.AddField(
            model_name='tyreset',
            name='used_in_sessions',
            field=models.ManyToManyField(blank=True, related_name='used_tyre_sets', to='Tyres_App.weekendsession'),
        ),
        migrations.CreateModel(
            name='SessionReturn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sets_to_return', models.IntegerField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tyres_App.weekendsession')),
                ('weekend_format', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session_returns', to='Tyres_App.weekendformat')),
            ],
        ),
        migrations.AddField(
            model_name='raceweekend',
            name='weekend_format',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='race_weekends', to='Tyres_App.weekendformat'),
        ),
    ]
