import pprint, time

from celery import shared_task
from celery.decorators import task

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

import django_filters

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework import filters
from rest_framework import status
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
    DjangoModelPermissions,
    DjangoObjectPermissions,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)

from impedans_expert.users.models import User
from impedans_expert.expert.models import (
    Chamber,
    ChamberProperty,
    Customer,
    Data,
    Marker,
    Parameter,
    SensorParameter,
    Sensor,
    SensorType,
)

from impedans_expert.expert.api.serializers import (
    ChamberCreateSerializer,
    ChamberDetailSerializer,
    ChamberListSerializer,
    ChamberPropertiesCreateSerializer,
    ChamberPropertiesDetailSerializer,
    ChamberPropertiesListSerializer,
    CustomerCreateSerializer,
    CustomerDetailSerializer,
    CustomerListSerializer,
    DataCreateSerializer,
    DataDetailSerializer,
    DataListSerializer,
    MarkerCreateSerializer,
    MarkerDetailSerializer,
    MarkerListSerializer,
    ParameterCreateSerializer,
    ParameterDetailSerializer,
    ParameterListSerializer,
    SensorCreateSerializer,
    SensorDetailSerializer,
    SensorListSerializer,
    SensorTypeCreateSerializer,
    SensorTypeDetailSerializer,
    SensorTypeListSerializer,
)

from .pagination import (
    ExpertPageNumberPagination,
)

from .permissions import (
    IsOwnerOrAdmin,
    IsSensor
)

from .tasks import create

##########################################################################################
# Define API views for Chamber related operations, create, delete, edit, update and list #
##########################################################################################

class ChamberCreateAPIView(CreateAPIView):
    queryset = Chamber.objects.all()
    serializer_class = ChamberCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            customer = Customer.objects.get(company_name=request.data["customer"])
            request.data["customer"] = customer.id
        except:
            print("Customer not registered.")

        serializer = ChamberCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class ChamberDeleteAPIView(DestroyAPIView):
    queryset = Chamber.objects.all()
    serializer_class = ChamberListSerializer
    permission_classes = [IsAuthenticated]

class ChamberDetailAPIView(RetrieveAPIView):
    queryset = Chamber.objects.all()
    serializer_class = ChamberDetailSerializer
    permission_classes = [IsAuthenticated]

class ChamberListAPIView(ListAPIView):
    queryset = Chamber.objects.all()
    queryset = queryset.prefetch_related('customer')
    serializer_class = ChamberListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'chamber_name', 'customer')
    # pagination_class = ExpertPageNumberPagination
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly]

class ChamberUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Chamber.objects.all()
    serializer_class = ChamberListSerializer
    permission_classes = [IsAuthenticated]

#####################################################################################################
# Define API views for Chamber Properties related operations, create, delete, edit, update and list #
#####################################################################################################

class ChamberPropertiesCreateAPIView(CreateAPIView):
    queryset = ChamberProperty.objects.all()
    serializer_class = ChamberPropertiesCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            chamber = Chamber.objects.get(chamber_name=request.data["chamber"])
            request.data["chamber"] = chamber.id
        except:
            print("Invalid chamber.")

        serializer = ChamberPropertiesCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class ChamberPropertiesDeleteAPIView(DestroyAPIView):
    queryset = ChamberProperty.objects.all()
    serializer_class = ChamberPropertiesListSerializer
    permission_classes = [IsAuthenticated]

class ChamberPropertiesDetailAPIView(RetrieveAPIView):
    queryset = ChamberProperty.objects.all()
    serializer_class = ChamberPropertiesDetailSerializer
    permission_classes = [IsAuthenticated]

class ChamberPropertiesListAPIView(ListAPIView):
    queryset = ChamberProperty.objects.all()
    queryset = queryset.prefetch_related('chamber')
    serializer_class = ChamberPropertiesListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'chamber', 'property_name', 'property_value')
    # pagination_class = ExpertPageNumberPagination
    permission_classes = [IsAuthenticated]

class ChamberPropertiesUpdateAPIView(RetrieveUpdateAPIView):
    queryset = ChamberProperty.objects.all()
    serializer_class = ChamberPropertiesListSerializer
    permission_classes = [IsAuthenticated]

###########################################################################################
# Define API views for Customer related operations, create, delete, edit, update and list #
###########################################################################################

class CustomerCreateAPIView(CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.data["user"])
            request.data["user"] = user.id
        except:
            print("Invalid user.")

        serializer = CustomerCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class CustomerDeleteAPIView(DestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer
    permission_classes = [IsAuthenticated]

class CustomerDetailAPIView(RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerDetailSerializer
    permission_classes = [IsAuthenticated]

class CustomerListAPIView(ListAPIView):
    queryset = Customer.objects.all()
    queryset = queryset.prefetch_related('user')
    serializer_class = CustomerListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'company_name', 'contact_name', 'contact_email', 'user')
    # pagination_class = ExpertPageNumberPagination
    permission_classes = [IsAuthenticated]

class CustomerUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer
    permission_classes = [IsAuthenticated]

#######################################################################################
# Define API views for Data related operations, create, delete, edit, update and list #
#######################################################################################

class DataCreateAPIView(CreateAPIView):
    # queryset = Data.objects.all()
    # queryset = queryset.prefetch_related('sensor', 'parameter')
    # queryset = DataCreateSerializer.setup_eager_loading(queryset)
    # post_data = DataCreateSerializer(queryset, many=True).data
    # serializer_class = DataCreateSerializer
    permission_classes = [IsSensor]

    def create(self, request, *args, **kwargs):
        request_data = dict(request.data)
        create.delay(request_data)
        return Response(status=status.HTTP_200_OK)

    # def create(self, request, *args, **kwargs):

    #     try:
    #         sensor = Sensor.objects.get(serial_number=request.data["data_source"])
    #         request.data["data_source"] = sensor.id
    #     except Sensor.DoesNotExist:
    #         print("Sensor serial number " + str(request.data["data_source"]) + " not registered.")
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    #     dataDict = dict(request.data)
    #     for param in dataDict['parameters']:
    #         Parameter.objects.get_or_create(parameter_name=param, parameter_position="None")

    #     final_data = []
    #     for data in dataDict['data_array']:
    #         zipped = zip(dataDict['parameters'], data['values'])
    #         for parameter, value in zipped:
    #             parameter = Parameter.objects.get(parameter_name=parameter)
    #             new_data = Data(sensor=sensor, parameter=parameter, time=data["time"], parameter_value=value)
    #             final_data.append(new_data)
    #     Data.objects.bulk_create(final_data)
    #     return Response(status=status.HTTP_200_OK)

    # def create(self, request, *args, **kwargs):
    #     queryset = Data.objects.all()
    #     queryset = DataCreateSerializer.setup_eager_loading(queryset)
    #     # serializer_class = DataCreateSerializer

    #     try:
    #         sensor = Sensor.objects.get(serial_number=request.data["data_source"])
    #         request.data["data_source"] = sensor.id
    #     except Sensor.DoesNotExist:
    #         print("Sensor serial number " + str(request.data["data_source"]) + " not registered.")
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    #     dataDict = dict(request.data)
    #     for param in dataDict['parameters']:
    #         Parameter.objects.get_or_create(parameter_name=param, parameter_position="None")

    #     final_data = []
    #     for data in dataDict['data_array']:
    #         zipped = zip(dataDict['parameters'], data['values'])
    #         for parameter, value in zipped:
    #             parameter = Parameter.objects.get(parameter_name=parameter)
    #             final_data.append({
    #                 "sensor": sensor.id,
    #                 "parameter": parameter.id,
    #                 "time": data['time'],
    #                 "parameter_value": value
    #             })
    #     serializer = DataCreateSerializer(data=final_data, many=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(status=status.HTTP_200_OK)
    #     return Response(serializer.errors)

class DataDeleteAPIView(DestroyAPIView):
    queryset = Data.objects.all()
    serializer_class = DataListSerializer
    permission_classes = [IsAuthenticated]

class DataDetailAPIView(RetrieveAPIView):
    queryset = Data.objects.all()
    serializer_class = DataDetailSerializer
    permission_classes = [IsAuthenticated]

class DataFilter(django_filters.rest_framework.FilterSet):
    time__gte = django_filters.IsoDateTimeFilter(name="time", lookup_expr='gte')
    time__lte = django_filters.IsoDateTimeFilter(name="time", lookup_expr='lte')
    class Meta:
        model = Data
        fields = ['id', 'time', 'time__gte', 'time__lte', 'sensor_parameter', 'parameter_value']

class DataListAPIView(ListAPIView):
    queryset = Data.objects.all()
    queryset = queryset.prefetch_related('sensor_parameter')
    serializer_class = DataListSerializer
    time__gte = django_filters.DateTimeFilter(name="time", lookup_expr='gte')
    time__lte = django_filters.DateTimeFilter(name="time", lookup_expr='lte')
    filter_backends = (OrderingFilter, DjangoFilterBackend, )
    # filter_fields = ('id', 'time', 'time__lte', 'time__gte', 'sensor', 'parameter', 'parameter_value')
    ordering_fields = ('id', 'sensor_parameter', 'parameter_value', 'time')
    ordering=("id")
    filter_class = DataFilter
    # pagination_class = ExpertPageNumberPagination
    permission_classes = [IsAuthenticated]

class DataUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Data.objects.all()
    serializer_class = DataListSerializer
    permission_classes = [IsAuthenticated]

#########################################################################################
# Define API views for Marker related operations, create, delete, edit, update and list #
#########################################################################################

class MarkerCreateAPIView(CreateAPIView):
    queryset = Marker.objects.all()
    serializer_class = MarkerCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            chamber = Chamber.objects.get(chamber_name=request.data["chamber"])
            request.data["chamber"] = chamber.id
        except:
            print("Invalid chamber.")

        serializer = MarkerCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class MarkerDeleteAPIView(DestroyAPIView):
    queryset = Marker.objects.all()
    serializer_class = MarkerListSerializer
    permission_classes = [IsAuthenticated]

class MarkerDetailAPIView(RetrieveAPIView):
    queryset = Marker.objects.all()
    serializer_class = MarkerDetailSerializer
    permission_classes = [IsOwnerOrAdmin]

class MarkerListAPIView(ListAPIView):
    queryset = Marker.objects.all()
    queryset = queryset.prefetch_related('chamber')
    serializer_class = MarkerListSerializer 
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'time', 'chamber', 'marker_name', 'marker_string')
    # pagination_class = ExpertPageNumberPagination
    permission_classes = [IsAuthenticated]

    def list(self, request):
       user = User.objects.get(username=request.user)
       customer = Customer.objects.get(user=user)
       chambers = Chamber.objects.filter(customer=customer)
       queryset = Marker.objects.filter(chamber__in=chambers)
       serializer = MarkerListSerializer(queryset, many=True, context={'request':request})
       return Response(serializer.data)

class MarkerUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Marker.objects.all()
    serializer_class = MarkerListSerializer
    permission_classes = [IsAuthenticated]

############################################################################################
# Define API views for Parameter related operations, create, delete, edit, update and list #
############################################################################################

class ParameterCreateAPIView(CreateAPIView):
    queryset = Parameter.objects.all()
    serializer_class = ParameterCreateSerializer
    permission_classes = [IsAuthenticated]

class ParameterDeleteAPIView(DestroyAPIView):
    queryset = Parameter.objects.all()
    serializer_class = ParameterListSerializer
    permission_classes = [IsAuthenticated]

class ParameterDetailAPIView(RetrieveAPIView):
    queryset = Parameter.objects.all()
    serializer_class = ParameterDetailSerializer
    permission_classes = [IsAuthenticated]

class ParameterListAPIView(ListAPIView):
    queryset = Parameter.objects.all()
    serializer_class = ParameterListSerializer 
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'parameter_name', 'parameter_type', 'parameter_unit')
    # pagination_class = ExpertPageNumberPagination
    permission_classes = [IsAuthenticated]

class ParameterUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Parameter.objects.all()
    serializer_class = ParameterListSerializer
    permission_classes = [IsAuthenticated]

#########################################################################################
# Define API views for Sensor related operations, create, delete, edit, update and list #
#########################################################################################

class SensorCreateAPIView(CreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            chamber = Chamber.objects.get(chamber_name=request.data["chamber"])
            request.data["chamber"] = chamber.id
        except:
            print("Invalid chamber.")

        # customer = Customer.objects.get(company_name=request.data["customer"])
        # print("-----------------------------------------------------------------")
        # print(request.data["customer"])
        # print("-----------------------------------------------------------------")
        # print(customer.id)
        # print("-----------------------------------------------------------------")

        serializer = SensorCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class SensorDeleteAPIView(DestroyAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorListSerializer
    permission_classes = [IsAuthenticated]

class SensorDetailAPIView(RetrieveAPIView):
    # queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        owner = self.request.user
        return Sensor.objects.filter(owner=owner)

class SensorListAPIView(ListAPIView):
    queryset = Sensor.objects.all()
    queryset = queryset.prefetch_related('chamber', 'sensor_type')
    serializer_class = SensorListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'chamber', 'sensor_type', 'serial_number')
    # pagination_class = ExpertPageNumberPagination
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     owner = self.request.user
    #     return Sensor.objects.filter(owner=owner)

class SensorUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer
    permission_classes = [IsAuthenticated]

##############################################################################################
# Define API views for Sensor Type related operations, create, delete, edit, update and list #
##############################################################################################

class SensorTypeCreateAPIView(CreateAPIView):
    queryset = SensorType.objects.all()
    serializer_class = SensorTypeCreateSerializer
    permission_classes = [IsAuthenticated]

class SensorTypeDeleteAPIView(DestroyAPIView):
    queryset = SensorType.objects.all()
    serializer_class = SensorTypeListSerializer
    permission_classes = [IsAuthenticated]

class SensorTypeDetailAPIView(RetrieveAPIView):
    queryset = SensorType.objects.all()
    serializer_class = SensorTypeDetailSerializer
    permission_classes = [IsAuthenticated]

class SensorTypeListAPIView(ListAPIView):
    queryset = SensorType.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'sensor_type',)
    # pagination_class = ExpertPageNumberPagination
    permission_classes = [IsAuthenticated]

    def list(self, request):
       user = User.objects.get(username=request.user)
       customer = Customer.objects.get(user=user)
       chambers = Chamber.objects.filter(customer=customer)
       queryset = Sensor.objects.filter(chamber__in=chambers)
       serializer = SensorTypeListSerializer(queryset, many=True, context={'request':request})
       return Response(serializer.data)

class SensorTypeUpdateAPIView(RetrieveUpdateAPIView):
    queryset = SensorType.objects.all()
    serializer_class = SensorTypeDetailSerializer
    permission_classes = [IsAuthenticated]