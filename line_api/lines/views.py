from django.contrib.auth.models import User

from rest_framework import permissions
from rest_framework import viewsets

from .models import Line, Announcement, Meeting, Task
from .serializers import LineSerializer, UserSerializer
from .serializers import AnnouncementSerializer, MeetingSerializer, TaskSerializer
from .permissions import IsOwnerOrReadOnly


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides 'list' and 'detail' views of users.

    Authenticated users can see list, details of all active users.
    """
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LineViewSet(viewsets.ModelViewSet):
    """
    Provides 'list', 'create', 'retrieve', 'update' and
    'destroy' actions for lines.

    Authenticated users can see list, details of all created lines.

    Authenticated users can only edit their own lines.
    """
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Line.objects.all()
    serializer_class = LineSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    Provides 'list', 'create', 'retrieve', 'update' and
    'destroy' actions for announcements.

    Authenticated users can see list, details of all created announcements.

    Authenticated users can create announcements, add them to
    owned lines and edit them.
    """
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MeetingViewSet(viewsets.ModelViewSet):
    """
    Provides 'list', 'create', 'retrieve', 'update' and
    'destroy' actions for meetings.

    Authenticated users can see list, details of all created meetings.

    Authenticated users can create meetings, add them to
    owned lines and edit them.
    """
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    """
    Provides 'list', 'create', 'retrieve', 'update' and
    'destroy' actions for tasks.

    Authenticated users can see list, details of all created tasks.

    Authenticated users can create tasks, add them to
    owned lines and edit them.
    """
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)