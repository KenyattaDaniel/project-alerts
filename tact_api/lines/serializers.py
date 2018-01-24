from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Line, Announcement, Event, Task


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Convert User model instances' native Python datatypes into and from JSON.
    """
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'lines')


class LineSerializer(serializers.HyperlinkedModelSerializer):
    """
    Convert Line model instances' native Python datatypes into and from JSON.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    announcements = serializers.HyperlinkedRelatedField(many=True, view_name='announcement-detail',
                                                        read_only=True)
    events = serializers.HyperlinkedRelatedField(many=True, view_name='event-detail',
                                                 read_only=True)
    tasks = serializers.HyperlinkedRelatedField(many=True, view_name='task-detail',
                                                read_only=True)

    class Meta:
        model = Line
        fields = ('url', 'id', 'owner', 'created', 'modified', 'title', 'announcements', 'events',
                  'tasks')

    def create_line(self, validated_data):
        """
        create and return a new Line object with validated data.
        """
        return Line.objects.create(**validated_data)

    def update_line(self, instance, validated_data):
        """
        update and return an existing line object with validated.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance


class AnnouncementSerializer(serializers.ModelSerializer):
    """
    Convert Announcement model instances' native Python datatypes into and from JSON.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Announcement
        fields = ('url', 'id', 'owner', 'created', 'modified', 'title', 'desc', 'line')

    def get_fields(self, *args, **kwargs):
        """
        create and return a new Announcement object (linked to a user Line) with validated data.

        update and return an existing Announcement object with validated data.
        """
        fields = super(AnnouncementSerializer, self).get_fields(*args, **kwargs)
        view = self.context['view']
        owner = view.request.user
        fields['line'].queryset = fields['line'].queryset.filter(owner=owner)
        return fields


class EventSerializer(serializers.ModelSerializer):
    """
    Convert Event model instances' native Python datatypes into and from JSON.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Event
        fields = ('url', 'id', 'owner', 'created', 'modified', 'title', 'desc', 'start',
                  'end', 'line')

    def get_fields(self, *args, **kwargs):
        """
        create and return a new Event object (linked to a user owned Line) with validated data.

        update and return an existing Event object with validated data.
        """
        fields = super(EventSerializer, self).get_fields(*args, **kwargs)
        view = self.context['view']
        owner = view.request.user
        fields['line'].queryset = fields['line'].queryset.filter(owner=owner)
        return fields


class TaskSerializer(serializers.ModelSerializer):
    """
    Convert Task model instances' native Python datatypes into and from JSON.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = ('url', 'id', 'owner', 'created', 'modified', 'title', 'desc', 'due', 'line')

    def get_fields(self, *args, **kwargs):
        """
        create and return a new Task object (linked to a user owned Line) with validated data.

        update and return an existing Task object with validated data.
        """
        fields = super(TaskSerializer, self).get_fields(*args, **kwargs)
        view = self.context['view']
        owner = view.request.user
        fields['line'].queryset = fields['line'].queryset.filter(owner=owner)
        return fields
