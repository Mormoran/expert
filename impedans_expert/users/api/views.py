from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView, 
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from impedans_expert.users.models import User

from impedans_expert.users.api.serializers import (
    UserCreateSerializer,
    UserDetailSerializer,
    UserListSerializer
)

from .pagination import (
    ExpertPageNumberPagination,
)

from .permissions import IsOwnerOrReadOnly

##########################################################################################
# Define API views for Chamber related operations, create, delete, edit, update and list #
##########################################################################################

class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated]

class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'name')
    pagination_class = ExpertPageNumberPagination

class UserUpdateAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]