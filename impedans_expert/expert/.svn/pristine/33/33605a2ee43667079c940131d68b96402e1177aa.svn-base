from celery import shared_task
from celery.decorators import task

from rest_framework.response import Response
from rest_framework import status

from impedans_expert.expert.models import Chamber, Parameter, SensorParameter, Sensor, Data

from impedans_expert.expert.api.serializers import DataCreateSerializer

# from xxxxxxxxxxxx import prepare_z_score_run


# @task(name='POST request Data point.')
# def create(request):
#     queryset = Data.objects.all()
#     queryset = DataCreateSerializer.setup_eager_loading(queryset)
#     serializer_class = DataCreateSerializer

#     try:
#         sensor = Sensor.objects.get(serial_number=request["data_source"])
#         request["data_source"] = sensor.id
#     except Sensor.DoesNotExist:
#         print("Sensor serial number " + str(request["data_source"]) + " not registered.")
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     dataDict = dict(request)
#     for param in dataDict['parameters']:
#         Parameter.objects.get_or_create(parameter_name=param, parameter_position="None")

#     final_data = []
#     for data in dataDict['data_array']:
#         zipped = zip(dataDict['parameters'], data['values'])
#         for parameter, value in zipped:
#             # parameter = Parameter.objects.get_or_create(parameter_name=parameter, parameter_position="None")[0]
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
#     #     return Response(status=status.HTTP_200_OK)
#     # return Response(serializer.errors)

@task(name='POST request Data point.')
def create(request):
    try:
        sensor = Sensor.objects.get(serial_number=request["data_source"])
        request["data_source"] = sensor.id
    except Sensor.DoesNotExist:
        print("Sensor serial number " + str(request["data_source"]) + " not registered.")
        return Response(status=status.HTTP_404_NOT_FOUND)

    dataDict = dict(request)
    for param in dataDict['parameters']:
        parameter = Parameter.objects.get_or_create(parameter_name=param)[0]
        sensor_parameter = SensorParameter.objects.get_or_create(sensor=sensor, parameter=parameter, parameter_name_userdef=parameter.parameter_name)
        
    final_data = []

    # TODO: Reorganize DB calls to reduce amount of calls

    for data in dataDict['data_array']:
        zipped = zip(dataDict['parameters'], data['values'])
        for parameter, value in zipped:
            parameter_instance = Parameter.objects.get(parameter_name=parameter)
            sensor_parameter = SensorParameter.objects.get(parameter=parameter_instance, sensor=sensor)
            if sensor_parameter.live_value != value:
                sensor_parameter.live_value=value
                sensor_parameter.save()
                # print(sensor_parameter.live_value)
            new_data = Data(sensor_parameter=sensor_parameter, time=data["time"], parameter_value=value)
            final_data.append(new_data)
    Data.objects.bulk_create(final_data)