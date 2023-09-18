# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import TyreSet, WeekendSession

# Signal to update WeekendSession model after a TyreSet is saved
@receiver(post_save, sender=TyreSet)
def update_weekend_session_after_save(sender, instance, **kwargs):
    # Dictionary to map TyreSet type to corresponding field in WeekendSession
    update_fields = {
        'Soft': 'sets_to_return_soft',
        'Medium': 'sets_to_return_medium',
        'Hard': 'sets_to_return_hard',
    }

    # If this TyreSet has a planned session for its return
    if instance.planned_return_session:
        session = instance.planned_return_session
        tyre_field_to_update = update_fields.get(instance.type)
        if tyre_field_to_update:
            # Calculate new count of TyreSets of this type planned to return in this session
            new_count = TyreSet.objects.filter(planned_return_session=session, type=instance.type).count()
            setattr(session, tyre_field_to_update, new_count) # Update the field
            session.save() # Save the session with updated information

    # Handle case where the planned_return_session was changed
    orig_session = getattr(instance, '_orig_planned_return_session', None)
    if orig_session:
        tyre_field_to_update = update_fields.get(instance.type)
        if tyre_field_to_update:
            # Update the original session with new count
            new_count = TyreSet.objects.filter(planned_return_session=orig_session, type=instance.type).count()
            setattr(orig_session, tyre_field_to_update, new_count)
            orig_session.save()  # Save the session with updated information

# Signal to update WeekendSession model after a TyreSet is deleted
@receiver(post_delete, sender=TyreSet)
def update_weekend_session_after_delete(sender, instance, **kwargs):
    # If this TyreSet had a planned session for its return
    if instance.planned_return_session:
        session = instance.planned_return_session
        # Dictionary to map TyreSet type to corresponding field in WeekendSession
        update_fields = {
            'Soft': 'sets_to_return_soft',
            'Medium': 'sets_to_return_medium',
            'Hard': 'sets_to_return_hard',
        }
        tyre_field_to_update = update_fields.get(instance.type)
        if tyre_field_to_update:
            # Update the count of TyreSets of this type planned for return in this session
            setattr(session, tyre_field_to_update, TyreSet.objects.filter(planned_return_session=session, type=instance.type).count())
            session.save()
