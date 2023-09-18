from django.db import models

# Car model
class Car(models.Model):
    name = models.CharField(max_length=255)

# TyreSet model
class TyreSet(models.Model):
    TYRE_CHOICES = [
        ('Soft', 'Soft'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    STATE_CHOICES = [
        ('New', 'New'),
        ('Used', 'Used'),
    ]
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=10, choices=TYRE_CHOICES)
    state = models.CharField(max_length=10, choices=STATE_CHOICES)
    car = models.ForeignKey(Car, related_name='tyre_sets', on_delete=models.CASCADE, null=True, blank=True)
    planned_return_session = models.ForeignKey('WeekendSession', related_name='planned_return_tyres',
                                               on_delete=models.SET_NULL, null=True)
    used_in_sessions = models.ManyToManyField('WeekendSession', related_name='used_tyres', blank=True,null=True)
    def save(self, *args, **kwargs):

        if self.pk is not None:
            orig = TyreSet.objects.get(pk=self.pk)
            self._orig_planned_return_session = orig.planned_return_session
        super().save(*args, **kwargs)

# RaceWeekend model
class RaceWeekend(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    weekend_format = models.ForeignKey('WeekendFormat', related_name='race_weekends', on_delete=models.SET_NULL, null=True)
    cars = models.ManyToManyField(Car, related_name='race_weekends')

# WeekendSession model
class WeekendSession(models.Model):
    name = models.CharField(max_length=255)
    custom_name = models.CharField(max_length=255, null=True, blank=True)
    is_race_session = models.BooleanField(default=False)
    race_weekend = models.ForeignKey(RaceWeekend, related_name='sessions', on_delete=models.CASCADE, null=True, blank=True)
    sets_to_return_soft = models.IntegerField(default=0)
    sets_to_return_medium = models.IntegerField(default=0)
    sets_to_return_hard = models.IntegerField(default=0)
    weekend_format = models.ForeignKey('WeekendFormat', related_name='weekend_sessions', on_delete=models.CASCADE)



# WeekendFormat model
class WeekendFormat(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    total_sets = models.IntegerField()
    hard_sets = models.IntegerField()
    medium_sets = models.IntegerField()
    soft_sets = models.IntegerField()

# WeekendTemplate model
class WeekendTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    total_sets = models.IntegerField()
    hard_sets = models.IntegerField()
    medium_sets = models.IntegerField()
    soft_sets = models.IntegerField()
    sessions = models.ManyToManyField(WeekendSession, related_name='weekend_templates')
    sessions_json = models.TextField(blank=True, null=True)

