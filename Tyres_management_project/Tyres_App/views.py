from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import WeekendFormat, WeekendSession, TyreSet
from .serializers import WeekendFormatSerializer, WeekendSessionSerializer, TyreSetSerializer, WeekendTemplateSerializer  # 引入新的序列化器
from rest_framework.decorators import action
from django.db.models import Q
from .models import WeekendFormat, WeekendSession, TyreSet, WeekendTemplate
from django.db import models
from django.core.serializers import serialize
from django.db.models import F
from django.core.serializers import deserialize
import logging

# Configure logging
logger = logging.getLogger(__name__)


class WeekendFormatViewSet(viewsets.ModelViewSet):
    queryset = WeekendFormat.objects.all()
    serializer_class = WeekendFormatSerializer

    # Method to create or update tyre sets
    def create_or_update_tyres(self, weekend_format):

        # Delete all existing TyreSets
        TyreSet.objects.all().delete()

        for i in range(weekend_format.soft_sets):
            TyreSet.objects.create(type='Soft', state='New')
        for i in range(weekend_format.medium_sets):
            TyreSet.objects.create(type='Medium', state='New')
        for i in range(weekend_format.hard_sets):
            TyreSet.objects.create(type='Hard', state='New')

    # Create a new WeekendFormat
    def create(self, request, *args, **kwargs):
        weekend_format = None

        # Check if a WeekendFormat with id=1 exists
        try:
            weekend_format = WeekendFormat.objects.get(id=1)
            serializer = self.get_serializer(weekend_format, data=request.data)
        except WeekendFormat.DoesNotExist:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        # Update or create a new WeekendFormat based on if it exists or not
        if weekend_format:
            self.perform_update(serializer)
        else:
            self.perform_create(serializer)
            weekend_format = WeekendFormat.objects.get(id=serializer.data['id'])

        self.create_or_update_tyres(weekend_format)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Update an existing WeekendFormat
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        self.create_or_update_tyres(instance)
        return Response(serializer.data)

    # Custom action to save a weekend as a template
    @action(detail=False, methods=['POST'])
    def save_weekend_template(self, request, *args, **kwargs):
        template_name = request.data.get('template_name')

        # Check if the template name already exists
        if WeekendTemplate.objects.filter(name=template_name).exists():
            return Response({"error": "Template name already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the most recent WeekendFormat
        try:
            weekend_format = WeekendFormat.objects.latest('id')
        except WeekendFormat.DoesNotExist:
            return Response({"error": "WeekendFormat does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        sessions = WeekendSession.objects.filter(weekend_format=weekend_format)
        sessions_json = serialize('json', sessions)

        weekend_template = WeekendTemplate.objects.create(
            name=template_name,
            description=f"Template description for {weekend_format.name}",
            total_sets=weekend_format.total_sets,
            hard_sets=weekend_format.hard_sets,
            medium_sets=weekend_format.medium_sets,
            soft_sets=weekend_format.soft_sets,
            sessions_json=sessions_json
        )

        weekend_template.sessions.set(sessions)
        weekend_template.save()
        return Response({"message": "Template saved successfully"}, status=status.HTTP_201_CREATED)





    @action(detail=False, methods=['POST'])
    def apply_weekend_template(self, request, *args, **kwargs):
        template_id = request.data.get('template_id')

        try:
            template = WeekendTemplate.objects.get(id=template_id)
        except WeekendTemplate.DoesNotExist:
            return Response({"error": "Template does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new WeekendFormat object
        weekend_format = WeekendFormat.objects.create(
            name=template.name,
            description=template.description,
            total_sets=template.total_sets,
            hard_sets=template.hard_sets,
            medium_sets=template.medium_sets,
            soft_sets=template.soft_sets,
        )

        # Deserialize the stored session data and re-create the sessions
        for deserialized_object in deserialize("json", template.sessions_json):


            deserialized_object.object.weekend_format = weekend_format
            deserialized_object.save()

            session_check = WeekendSession.objects.get(id=deserialized_object.object.id)


            session = deserialized_object.object
            session.weekend_format = weekend_format  # explicitly set the relation to the new WeekendFormat

            # Assuming these fields are in the deserialized object
            session.sets_to_return_soft = deserialized_object.object.sets_to_return_soft
            session.sets_to_return_medium = deserialized_object.object.sets_to_return_medium
            session.sets_to_return_hard = deserialized_object.object.sets_to_return_hard

            session.save()

        self.create_or_update_tyres(weekend_format)

        return Response({"message": "Template applied successfully"}, status=status.HTTP_201_CREATED)

    # Custom action to clear all data
    @action(detail=False, methods=['POST'])
    def clear_all_data(self, request, *args, **kwargs):

        WeekendFormat.objects.all().delete()

        WeekendSession.objects.all().delete()

        TyreSet.objects.all().delete()

        WeekendTemplate.objects.all().delete()

        return Response({"status": "All data cleared"}, status=status.HTTP_200_OK)

    # Custom action to clear all data but keep the templates
    @action(detail=False, methods=['POST'])
    def clear_all_data_keepTemplate(self, request, *args, **kwargs):

        WeekendFormat.objects.all().delete()

        WeekendSession.objects.all().delete()

        TyreSet.objects.all().delete()


        return Response({"status": "All data cleared but keep template"}, status=status.HTTP_200_OK)




# Define the WeekendTemplateViewSet class
class WeekendTemplateViewSet(viewsets.ModelViewSet):
    queryset = WeekendTemplate.objects.all().prefetch_related('sessions').order_by('id')

    serializer_class = WeekendTemplateSerializer

# Define the WeekendSessionViewSet class
class WeekendSessionViewSet(viewsets.ModelViewSet):
    queryset = WeekendSession.objects.all()
    serializer_class = WeekendSessionSerializer

    # Override the create method
    def create(self, request, *args, **kwargs):
        # Try to get the latest WeekendFormat, return 400 if not exists
        try:
            weekend_format = WeekendFormat.objects.latest('id')
        except WeekendFormat.DoesNotExist:
            return Response({"error": "WeekendFormat does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Clone request data and set weekend_format
        mutable_data = request.data.copy()
        mutable_data['weekend_format'] = weekend_format.id

        # Validate the serializer
        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)

        # Set the validated weekend_format to the serializer data
        serializer.validated_data['weekend_format'] = weekend_format
        self.perform_create(serializer)

        # Fetch and work on the newly created session
        session = WeekendSession.objects.get(id=serializer.instance.id)
        tyres_to_return_soft = session.sets_to_return_soft
        tyres_to_return_medium = session.sets_to_return_medium
        tyres_to_return_hard = session.sets_to_return_hard

        # Update planned_return_session for the available TyreSet instances
        for type_, count in [("Soft", tyres_to_return_soft), ("Medium", tyres_to_return_medium),
                             ("Hard", tyres_to_return_hard)]:
            tyre_sets = TyreSet.objects.filter(
                Q(type=type_) &
                Q(planned_return_session__isnull=True)
            )[:count]

            for tyre_set in tyre_sets:
                tyre_set.planned_return_session = session
                tyre_set.save()

        # Update the session with the new tyre set counts
        session.sets_to_return_soft = TyreSet.objects.filter(
            planned_return_session=session, type='Soft'
        ).count()
        session.sets_to_return_medium = TyreSet.objects.filter(
            planned_return_session=session, type='Medium'
        ).count()
        session.sets_to_return_hard = TyreSet.objects.filter(
            planned_return_session=session, type='Hard'
        ).count()
        session.save()


        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)




class TyreSetViewSet(viewsets.ModelViewSet):
    queryset = TyreSet.objects.all()
    serializer_class = TyreSetSerializer

    @action(detail=True, methods=['POST'])
    def update_tyre(self, request, pk=None):
        # Retrieve the TyreSet by primary key, return 404 if not found
        try:
            tyre_set = TyreSet.objects.get(pk=pk)
        except TyreSet.DoesNotExist:
            return Response({"error": "TyreSet does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Get data from request
        planned_return_session_id = request.data.get("planned_return_session")
        used_in_sessions = request.data.get("used_in_sessions")

        # If planned_return_session_id is provided, update the TyreSet's planned_return_session
        if planned_return_session_id is not None:
            try:
                session = WeekendSession.objects.get(id=planned_return_session_id)
                tyre_set.planned_return_session = session

                # Update the count of returned tyres in the planned return session
                update_fields = {
                    'hard': 'returned_hard_tyres',
                    'medium': 'returned_medium_tyres',
                    'soft': 'returned_soft_tyres',
                }

                tyre_field_to_update = update_fields.get(tyre_set.tyre_type)
                if tyre_field_to_update:

                    setattr(session, tyre_field_to_update, F(tyre_field_to_update) + 1)

                session.save()
                session.refresh_from_db()

            except WeekendSession.DoesNotExist:
                return Response({"error": "WeekendSession does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Update the TyreSet's used_in_sessions field
        if used_in_sessions is None:
            tyre_set.used_in_sessions.clear()
        elif isinstance(used_in_sessions, list):
            tyre_set.used_in_sessions.set(used_in_sessions)

        # Save the TyreSet and return the updated data
        tyre_set.save()
        serializer = TyreSetSerializer(tyre_set)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def list_tyres(self, request, *args, **kwargs):
        queryset = TyreSet.objects.all().order_by('id')
        serializer = TyreSetSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
