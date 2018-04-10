import os.path
import datetime
import glob
import csv

from datetime import datetime
from django.utils import timezone

from celery.decorators import task

from impedans_expert.expert.models import Chamber, Sensor, Marker, Data, Parameter
from impedans_expert.expert_import.models import Run, RunProperty


# create "temporary" classes used to cut out duplicate entries
# using calculated hash values for sensors, runs, runproperties
# markers and data
class TempSensor:
    def __init__(self, temp_chamber, temp_serial):
        self.chamber = temp_chamber
        self.serial_number = temp_serial

    def __key(self):
        return self.chamber, self.serial_number

    def __eq__(self, y):
        return isinstance(y, self.__class__) and self.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())


class TempRun:
    def __init__(self, temp_start, temp_end, temp_chamber):
        self.start = temp_start
        self.end = temp_end
        self.chamber = temp_chamber

    def __key(self):
        return self.start, self.end, self.chamber

    def __eq__(self, y):
        return isinstance(y, self.__class__) and self.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())


class TempRunProperties:
    def __init__(self, temp_start, temp_end, temp_chamber, property_type, property_value):
        self.start = temp_start
        self.end = temp_end
        self.chamber = temp_chamber
        self.type = property_type
        self.value = property_value

    def __key(self):
        return self.start, self.end, self.chamber, self.type, self.value

    def __eq__(self, y):
        return isinstance(y, self.__class__) and self.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())


class TempMarker:
    def __init__(self, temp_time, temp_chamber, temp_marker_name, temp_marker_string):
        self.time = temp_time
        self.chamber = temp_chamber
        self.marker_name = temp_marker_name
        self.marker_string = temp_marker_string

    def __key(self):
        return self.chamber, self.marker_name, self.marker_string

    def __eq__(self, y):
        return isinstance(y, self.__class__) and self.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())


class TempData:
    def __init__(self, temp_time, temp_sensor, temp_parameter, temp_value):
        self.time = temp_time
        self.sensor = temp_sensor
        self.parameter = temp_parameter
        self.value = temp_value

    def __key(self):
        return self.time, self.sensor, self.parameter, self.value

    def __eq__(self, y):
        return isinstance(y, self.__class__) and self.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())


# read the configuration file to get the column haeders for selecting the
# correct data
class CsvParser:

    chamber_name_keys = []
    timestamp_keys = []
    all_chambers = []
    all_chambers_query = []
    begin_file_time = None
    end_file_time = None
    parameters = []
    data_timezone = ""
    time_format = None
    run_time_format = None
    run_property_keys = []
    run_time_keys = []
    marker_keys = []
    data_keys = []
    num_of_properties = 0

    all_sensor_serial_numbers = set()
    all_sensors_query = None
    all_sensors = []
    # db date format -> "%Y-%m-%d %H:%M:%S.%f%Z"

    # read the configuration file
    def get_configuration(self, conf_file):
        config = {}
        # execute the file
        print("GETTING CONFIGURATION")
        exec(compile(open(conf_file, "rb").read(), conf_file, 'exec'), config)

        # set the list of parameter headers to be searched for in the parse file
        self.chamber_name_keys = config['chamber']

        self.timestamp_keys = config['time']
        self.time_format = config['time_format']

        self.run_time_keys = config['runs_times']
        self.run_time_format = config['run_time_format']

        self.run_property_keys = config['run_properties']

        self.marker_keys = config['markers_names']

        self.data_keys = config['data']

        self.data_timezone = config['timezone']

        del config

    # read a csv file
    # @staticmethod
    def read_csv_file(self, file_path):
        is_file = False
        while not is_file:
            if os.path.exists(file_path):
                is_file = True
        result_data = []

        with open(file_path) as csvfile:
            array = csv.DictReader(csvfile)
            for row in array:
                data = row
                result_data.append(data)
        return result_data

    # organize all data from the file into unique lists of data
    # later to be used for entries to the database
    def get_all_data_from_file(self, data):
        data_parameters = set()
        markers = []
        run_properties = set()
        run_times = set()
        sensors = set()
        chamber_names = []
        self.num_of_properties = len(self.run_property_keys)
        num_of_mark_types = len(self.marker_keys)

        # get all the parameter type for the data in the file
        for key in self.data_keys:
            self.parameters.append(Parameter.objects.get(parameter_name=key))

        # iterate through the csv file row by row
        for d, dat in enumerate(data):
            # get chamber_name
            chamber_name_parts = [dat[key] for key in self.chamber_name_keys]
            chamber_name = "".join(chamber_name_parts)
            chamber_names.append(chamber_name)

            # ============================================================
            # get times
            time_parts = [dat[key] for key in self.timestamp_keys]
            timestamp = " ".join(time_parts)
            timestamp = timestamp + self.data_timezone
            real_timestamp = datetime.strptime(timestamp, self.time_format)

            # get start and end times of the file
            if self.begin_file_time is None or self.begin_file_time > real_timestamp:
                self.begin_file_time = real_timestamp
            elif self.end_file_time is None or self.end_file_time < real_timestamp:
                self.end_file_time = real_timestamp

            # ============================================================
            # get sensors
            sensor_name = chamber_name + "_Data"
            self.all_sensor_serial_numbers.add(sensor_name)
            temp_sensor = TempSensor(chamber_name, sensor_name)
            sensors.add(temp_sensor)

            # ============================================================
            # get runs
            run_time = [(dat[key] + self.data_timezone) for key in self.run_time_keys]
            temp_run = TempRun(run_time[0], run_time[1], chamber_name)
            run_times.add(temp_run)

            # ============================================================
            # get run_properties
            for key in self.run_property_keys:
                temp_property = TempRunProperties(run_time[0], run_time[1], chamber_name, key, dat[key])
                run_properties.add(temp_property)

            # ============================================================
            # get markers
            for key in self.marker_keys:
                temp_marker = TempMarker(real_timestamp, chamber_name, key, dat[key])
                if len(markers) >= num_of_mark_types:
                    counter = 1
                    is_current_marker = False
                    while counter <= num_of_mark_types:
                        pos = 0 - counter
                        if temp_marker == markers[pos]:
                            is_current_marker = True
                        counter = counter + 1
                    if not is_current_marker:
                        markers.append(temp_marker)
                else:
                    markers.append(temp_marker)

            # ============================================================
            # get data
            for k, key in enumerate(self.data_keys):
                if dat[key] != "":
                    temp_data_point = TempData(real_timestamp, sensor_name, self.parameters[k], float(dat[key]))
                    data_parameters.add(temp_data_point)

            # ============================================================

        del data
        # return all the important data read from the file in arrays relevant to
        # different database tables
        return chamber_names, sensors, run_times, run_properties, markers, data_parameters

    # get or create all chamber objects from the file
    def create_chamber_instances(self, chamber_names, customer):
        # convert chamber_names to set
        chamber_set = set(chamber_names)
        for chamber_name in chamber_set:
            Chamber.objects.get_or_create(chamber_name=chamber_name, customer=customer)
        self.all_chambers_query = Chamber.objects.filter(chamber_name__in=chamber_set)
        self.all_chambers = list(self.all_chambers_query)
        del chamber_set

    # get or create all sensor objects from the file
    def create_sensor_instances(self, sensors):
        for sensor in sensors:
            sensor_chamber = Chamber.objects.get(chamber_name=sensor.chamber)
            Sensor.objects.get_or_create(serial_number=sensor.serial_number, chamber=sensor_chamber,
                                         sensor_type_id=1)
        del sensors
        self.all_sensors_query = Sensor.objects.filter(chamber_id__in=self.all_chambers,
                                                       serial_number__in=self.all_sensor_serial_numbers)
        self.all_sensors = list(self.all_sensors_query)

    # create all unique runs from the file, if duplicates already exist in the file exit
    # (file must have already been read)
    def create_run_instances(self, runs):
        runs_to_create = set()
        for run in runs:
            run_chamber = [chamber for chamber in self.all_chambers if chamber.chamber_name == run.chamber]
            runs_to_create.add(Run(start_time=datetime.strptime(run.start, self.run_time_format),
                                    end_time=datetime.strptime(run.end, self.run_time_format),
                                    chamber_id=run_chamber[0].id, file_id=68))
        del runs
        try:
            Run.objects.bulk_create(runs_to_create)
        except:
            print("DUPLICATES IN THE DB")
            return False
        return True

    # create all unique run properties from the file, if duplicates already exist in the file exit
    # (file must have already been read)
    def create_run_property_instances(self, run_properties):  # + runs
        # get all runs from the file
        file_runs_query = sorted(Run.objects.filter(chamber__in=self.all_chambers_query,
                                                     end_time__gte=self.begin_file_time,
                                                     start_time__lte=self.end_file_time), key=lambda r: r.start_time)
        # create a local copy of the query results
        file_runs = list(file_runs_query)
        del file_runs_query

        # create all unique properties
        properties_to_create = set()
        for p, run_property in enumerate(run_properties):
            # find the relevant chamber in the local list of all chambers in the file
            run_chamber = [chamber for chamber in self.all_chambers if chamber.chamber_name == run_property.chamber]
            current_run = None
            property_start = datetime.strptime(run_property.start, self.run_time_format)
            property_end = datetime.strptime(run_property.end, self.run_time_format)

            # find the run the property belongs to
            for run in file_runs:
                if run.start_time == property_start and \
                   run.end_time == property_end and \
                   run.chamber_id == run_chamber[0].id:
                    current_run = run
                    break
            if current_run is not None:
                # create run property
                properties_to_create.add(RunProperty(runs_id=current_run.id, property_name=run_property.type,
                                                       property_value=run_property.value))
        del file_runs
        del run_properties
        try:
            # write to database
            RunProperty.objects.bulk_create(properties_to_create)
        except:
            print("DUPLICATES IN THE DB")
            return False
        del properties_to_create
        return True

    # create all markers from the file, if duplicates already exist in the file exit
    # (file must have already been read)
    def create_marker_instances(self, markers):
        markers_to_create = set()
        for marker in markers:
            marker_chamber = [chamber for chamber in self.all_chambers if chamber.chamber_name == marker.chamber]
            markers_to_create.add(Marker(time=marker.time, marker_name=marker.marker_name,
                                         marker_string=marker.marker_string, chamber_id=marker_chamber[0].id))
        # commit the markers
        del markers
        try:
            Marker.objects.bulk_create(markers_to_create)
        except:
            print("DUPLICATES IN THE DB")
            return False
        return True

    # create all unique data points from the file, if duplicates already exist in the file exit
    # (file must have already been read)
    def create_data_instances(self, data_points):
        # commit
        data_to_create = set()

        for d, data_point in enumerate(data_points):
            sensor = [sensor for sensor in self.all_sensors if sensor.serial_number == data_point.sensor]

            data_to_create.add(Data(time=data_point.time, parameter_value=data_point.value,
                                    parameter_id=data_point.parameter.id, sensor_id=sensor[0].id))
        del data_points
        try:
            Data.objects.bulk_create(data_to_create)
        except:
            print("DUPLICATES IN THE DB")
            return False
        return True

@task(name="CSV parser process")
def run_csv_parser(customer, data_file, config_file):
    run_parser = CsvParser()
    run_parser.get_configuration(conf_file=config_file)
    read_data = run_parser.read_csv_file(file_path=data_file)
    file_data = run_parser.get_all_data_from_file(read_data)
    # ==========================================================
    # file data:
    # 0) Chamber Names	3) Run Properties
    # 1) Sensors	4) Markers
    # 2) Run		5) Data
    # ==========================================================

    del read_data

    run_parser.create_chamber_instances(file_data[0], customer)
    run_parser.create_sensor_instances(file_data[1])

    if not run_parser.create_run_instances(file_data[2]):
        print("File already exists, skipping the file")
    if not run_parser.create_run_property_instances(file_data[3]):
        print("File already exists, skipping the file")
    if not run_parser.create_marker_instances(file_data[4]):
        print("File already exists, skipping the file")
    if not run_parser.create_data_instances(file_data[5]):
        print("File already exists, skipping the file")

    del file_data
    
    return
