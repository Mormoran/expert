from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from django_filters.rest_framework import DjangoFilterBackend

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

from impedans_expert.expert_algorithms.models import (
    Algorithm,
    AlgorithmRun,
    AlgorithmRunResult,
    AlgorithmTimeResult,
    AlgorithmState
)

from impedans_expert.expert_import.models import Run

from impedans_expert.expert_algorithms.api.serializers import (
    AlgorithmCreateSerializer,
    AlgorithmDetailSerializer,
    AlgorithmListSerializer,
    AlgorithmRunCreateSerializer,
    AlgorithmRunDetailSerializer,
    AlgorithmRunListSerializer,
    AlgorithmRunResultsCreateSerializer,
    AlgorithmRunResultsDetailSerializer,
    AlgorithmRunResultsListSerializer,
    AlgorithmTimeResultsCreateSerializer,
    AlgorithmTimeResultsDetailSerializer,
    AlgorithmTimeResultsListSerializer,
    AlgorithmStateCreateSerializer,
    AlgorithmStateDetailSerializer,
    AlgorithmStateListSerializer,
)

from .pagination import (
    ExpertPageNumberPagination,
)

from .permissions import IsOwnerOrReadOnly

############################################################################################
# Define API views for Algorithm related operations, create, delete, edit, update and list #
############################################################################################

class AlgorithmCreateAPIView(CreateAPIView):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmCreateSerializer
    permission_classes = [IsAuthenticated]

class AlgorithmDeleteAPIView(DestroyAPIView):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmListSerializer

class AlgorithmDetailAPIView(RetrieveAPIView):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmDetailSerializer

class AlgorithmListAPIView(ListAPIView):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'algorithm_name', 'algorithm_src', 'algorithm_description')
    pagination_class = ExpertPageNumberPagination

class AlgorithmUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

################################################################################################
# Define API views for Algorithm Run related operations, create, delete, edit, update and list #
################################################################################################

class AlgorithmRunCreateAPIView(CreateAPIView):
    queryset = AlgorithmRun.objects.all()
    serializer_class = AlgorithmRunCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AlgorithmRunDeleteAPIView(DestroyAPIView):
    queryset = AlgorithmRun.objects.all()
    serializer_class = AlgorithmRunListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AlgorithmRunDetailAPIView(RetrieveAPIView):
    queryset = AlgorithmRun.objects.all()
    serializer_class = AlgorithmRunDetailSerializer

class AlgorithmRunListAPIView(ListAPIView):
    queryset = AlgorithmRun.objects.all()
    queryset = queryset.prefetch_related('algorithm', 'customer')
    serializer_class = AlgorithmRunListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'algorithm', 'customer', 'date_time')
    # pagination_class = ExpertPageNumberPagination

class AlgorithmRunUpdateAPIView(RetrieveUpdateAPIView):
    queryset = AlgorithmRun.objects.all()
    serializer_class = AlgorithmRunListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

########################################################################################################
# Define API views for Algorithm Run Results related operations, create, delete, edit, update and list #
########################################################################################################

class AlgorithmRunResultsCreateAPIView(CreateAPIView):
    queryset = AlgorithmRunResult.objects.all()
    serializer_class = AlgorithmRunResultsCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AlgorithmRunResultsDeleteAPIView(DestroyAPIView):
    queryset = AlgorithmRunResult.objects.all()
    serializer_class = AlgorithmRunResultsListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AlgorithmRunResultsDetailAPIView(RetrieveAPIView):
    queryset = AlgorithmRunResult.objects.all()
    serializer_class = AlgorithmRunResultsDetailSerializer

class AlgorithmRunResultsListAPIView(ListAPIView):
    queryset = AlgorithmRunResult.objects.all()
    queryset = queryset.prefetch_related('runs', 'algorithm_run', 'parameter')
    serializer_class = AlgorithmRunResultsListSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('id', 'algorithm_run', 'parameter', 'value', 'runs', 'start_time')
    ordering=("id")
    filter_fields = ('id', 'runs', 'algorithm_run', 'parameter', 'value')
    # pagination_class = ExpertPageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

class AlgorithmRunResultsUpdateAPIView(RetrieveUpdateAPIView):
    queryset = AlgorithmRunResult.objects.all()
    serializer_class = AlgorithmRunResultsListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

#########################################################################################################
# Define API views for Algorithm Time Results related operations, create, delete, edit, update and list #
#########################################################################################################

class AlgorithmTimeResultsCreateAPIView(CreateAPIView):
    queryset = AlgorithmTimeResult.objects.all()
    serializer_class = AlgorithmTimeResultsCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AlgorithmTimeResultsDeleteAPIView(DestroyAPIView):
    queryset = AlgorithmTimeResult.objects.all()
    serializer_class = AlgorithmTimeResultsListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AlgorithmTimeResultsDetailAPIView(RetrieveAPIView):
    queryset = AlgorithmTimeResult.objects.all()
    serializer_class = AlgorithmTimeResultsDetailSerializer

class AlgorithmTimeResultsListAPIView(ListAPIView):
    queryset = AlgorithmTimeResult.objects.all()
    queryset = queryset.prefetch_related('algorithm_run', 'parameter')
    serializer_class = AlgorithmTimeResultsListSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('id', 'algorithm_run', 'parameter', 'value', 'start_time', 'end_time', 'chamber')
    ordering=("id")
    filter_fields = ('id', 'algorithm_run', 'parameter', 'value', 'start_time', 'end_time', 'chamber')
    # pagination_class = ExpertPageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class AlgorithmTimeResultsUpdateAPIView(RetrieveUpdateAPIView):
    queryset = AlgorithmTimeResult.objects.all()
    serializer_class = AlgorithmTimeResultsListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

##################################################################################################
# Define API views for Algorithm State related operations, create, delete, edit, update and list #
##################################################################################################

class AlgorithmStateCreateAPIView(CreateAPIView):
    queryset = AlgorithmState.objects.all()
    serializer_class = AlgorithmStateCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AlgorithmStateDeleteAPIView(DestroyAPIView):
    queryset = AlgorithmState.objects.all()
    serializer_class = AlgorithmStateListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AlgorithmStateDetailAPIView(RetrieveAPIView):
    queryset = AlgorithmState.objects.all()
    serializer_class = AlgorithmStateDetailSerializer

class AlgorithmStateListAPIView(ListAPIView):
    queryset = AlgorithmState.objects.all()
    queryset = queryset.prefetch_related('algorithm_run')
    serializer_class = AlgorithmStateListSerializer 
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'algorithm_run', 'state')
    pagination_class = ExpertPageNumberPagination

class AlgorithmStateUpdateAPIView(RetrieveUpdateAPIView):
    queryset = AlgorithmState.objects.all()
    serializer_class = AlgorithmStateListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
