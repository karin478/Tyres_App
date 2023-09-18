from rest_framework import serializers
from .models import WeekendFormat, WeekendSession,TyreSet
from rest_framework import serializers
from .models import WeekendTemplate
import json

# Serializer for WeekendFormat model, to translate between model instances and data types like dictionaries
class WeekendFormatSerializer(serializers.ModelSerializer):
    # Meta class to specify which model and fields to use
    class Meta:
        model = WeekendFormat
        fields = ('id', 'name', 'description', 'total_sets', 'hard_sets', 'medium_sets', 'soft_sets')

# Serializer for WeekendSession model, to manage different sessions during a race weekend
class WeekendSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeekendSession
        fields = ('id', 'name', 'custom_name', 'is_race_session', 'sets_to_return_soft', 'sets_to_return_medium', 'sets_to_return_hard')

# Serializer for WeekendTemplate model, includes related WeekendSession models
class WeekendTemplateSerializer(serializers.ModelSerializer):
    # Adding a nested serialization for all related WeekendSession instances
    sessions = WeekendSessionSerializer(source='sessions.all', many=True, read_only=True)

    class Meta:
        model = WeekendTemplate
        fields = ['id','name', 'description', 'total_sets', 'hard_sets', 'medium_sets', 'soft_sets', 'sessions']

# Serializer for TyreSet model to manage individual sets of tires
class TyreSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TyreSet
        fields = '__all__'

    # Get the session Primary Keys where this TyreSet was used
    def get_used_in_sessions(self, obj):
        return [session.pk for session in obj.used_in_sessions.all()]

    # Custom method to validate the 'used_in_sessions' data field
    def to_internal_value(self, data):
        # Run validation using the base class's implementation
        internal_value = super().to_internal_value(data)
        used_in_sessions = data.get("used_in_sessions")
        if used_in_sessions is None or used_in_sessions == "None":
            internal_value["used_in_sessions"] = None
        return internal_value