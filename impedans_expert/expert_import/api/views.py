from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet

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

from impedans_expert.expert.models import (
    Chamber,
    ChamberProperty
)

from impedans_expert.expert_import.models import (
    RunProperty,
    Run,
)

from impedans_expert.expert_import.api.serializers import (
    RunsCreateSerializer,
    RunsDetailSerializer,
    RunsListSerializer,
    RunPropertiesCreateSerializer,
    RunPropertiesDetailSerializer,
    RunPropertiesListSerializer,
)

from .pagination import (
    RunsPageNumberPagination,
)

from .permissions import IsOwnerOrReadOnly


#########################################################################################
# Define custom mixin class to allow PUT requests to create objects if they don't exist #
#########################################################################################

class AllowPUTAsCreateMixin(object):
    """
    The following mixin class may be used in order to support PUT-as-create
    behavior for incoming requests.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object_or_none()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if instance is None:
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            lookup_value = self.kwargs[lookup_url_kwarg]
            extra_kwargs = {self.lookup_field: lookup_value}
            serializer.save(**extra_kwargs)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def get_object_or_none(self):
        try:
            return self.get_object()
        except Http404:
            if self.request.method == 'PUT':
                # For PUT-as-create operation, we need to ensure that we have
                # relevant permissions, as if this was a POST request.  This
                # will either raise a PermissionDenied exception, or simply
                # return None.
                self.check_permissions(clone_request(self.request, 'POST'))
            else:
                # PATCH requests where the object does not exist should still
                # return a 404 response.
                raise

#######################################################################################
# Define API views for Runs related operations, create, delete, edit, update and list #
#######################################################################################

class RunsCreateAPIView(CreateAPIView):
    queryset = Run.objects.all()
    queryset = queryset.prefetch_related('chamber')
    serializer_class = RunsCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            chamber = Chamber.objects.get(chamber_name=request.data["chamber"])
            request.data["chamber"] = chamber.id
        except:
            print("Invalid chamber name")

        serializer = RunsCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class RunsDeleteAPIView(DestroyAPIView):
    queryset = Run.objects.all()
    serializer_class = RunsListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class RunsDetailAPIView(RetrieveAPIView):
    queryset = Run.objects.all()
    serializer_class = RunsDetailSerializer

class RunsListAPIView(ListAPIView):
    queryset = Run.objects.all()
    queryset = queryset.prefetch_related('chamber')
    serializer_class = RunsListSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('id', 'chamber', 'start_time', 'end_time', 'recipe')
    ordering=("id")
    filter_fields = ('id', 'chamber', 'start_time', 'end_time', 'recipe')
    permission_classes = [IsAuthenticated]

class RunsUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Run.objects.all()
    serializer_class = RunsListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

#################################################################################################
# Define API views for Run Properties related operations, create, delete, edit, update and list #
#################################################################################################

class RunPropertiesCreateAPIView(CreateAPIView):
    queryset = RunProperty.objects.all()
    serializer_class = RunPropertiesCreateSerializer
    permission_classes = [IsAuthenticated]

class RunPropertiesDeleteAPIView(DestroyAPIView):
    queryset = RunProperty.objects.all()
    serializer_class = RunPropertiesListSerializer

class RunPropertiesDetailAPIView(RetrieveAPIView):
    queryset = RunProperty.objects.all()
    serializer_class = RunPropertiesDetailSerializer

class RunPropertiesListAPIView(ListAPIView):
    queryset = RunProperty.objects.all()
    queryset = queryset.prefetch_related('runs')
    serializer_class = RunPropertiesListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'runs', 'property_name', 'property_value')

class RunPropertiesUpdateAPIView(RetrieveUpdateAPIView):
    queryset = RunProperty.objects.all()
    serializer_class = RunPropertiesListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
