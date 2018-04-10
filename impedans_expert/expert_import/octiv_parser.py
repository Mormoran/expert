import dateutil.parser
import datetime
import os.path
from django.core.management.base import BaseCommand
from django.conf import settings

import time

from celery import shared_task
from celery.decorators import task

from impedans_expert.expert.models import *
from impedans_expert.expert_import.models import Run, RunProperty


# a class used to hash the parameter types and facilitate the use of
# sets to create a unique selection and prevent duplicate attempted Parameter entries
class ParameterData:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def __key(self):
        return self.name, self.position

    def __eq__(self, y):
        return isinstance(y, self.__class__) and self.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())


class OctivParser() :

    # passes in an array of data rows as strings from the file,
    # splits each row by value and returns a 2D array of the data from those rows
    def create_data_array(self, raw_data_list):
        data_array = []
        # split up every row by data point (seperated by the ";" delimiter)
        for n, rawData in enumerate(raw_data_list):
            row = raw_data_list[n].split(";")
            # if voltage or current values are zero skip the row. Do not record 0 values as they
            # indicate the process is not running and would skew statistical analysis
            # if float(row[2]) == 0 or float(row[4]) == 0:
            #     pass
            # else:

            # keep 0s to identify runs
            data_array.append(row)
        return data_array


    # read an octiv file seperating the information from the header
    # and the main block of data
    def read_octiv_file(self, file_path):
        is_file = False
        while not is_file:
            if os.path.exists(file_path):
                is_file = True
        with open(file_path, "r") as ins:
            array = []
            for line in ins:
                array.append(line)
            ins.close()
        file_name = os.path.basename(file_path)
        timestamp = None
        params = []  # this contains all of the parameters in the .dat file
        raw_data_list = []
        position = ""
        list_of_positions = []
        serial_num = ""
        all_data_from_file = []

        is_pulse = False
        number_of_buffer_points_skipped = 0
        # pulls all of the information required from the file
        for i, value in enumerate(array):
            value = value.strip(' \t\n\r')
            last_char = value[-1:]
            while last_char == ";":
                value = value[:-1]
                last_char = value[-1:]

            if "Created" in value:
                ts = value.split(";")
                time_string = ""
                # Determine whether the time format is ISO or non-standard
                if "T" in ts[1]:
                    timestamp = dateutil.parser.parse(ts[1])
                    print("TIME: ", timestamp)
                # Normal time stamp case
                else:
                    string_list = ts[1].split("-")
                    date_string_list = string_list[0].split("_")
                    if len(date_string_list) > 1:
                        time_string = date_string_list[0] + "-" + date_string_list[1] + "-" + date_string_list[2] \
                                      + " " + string_list[1] + ":" + string_list[2] + ":" + \
                                      string_list[3].rstrip() + ":00.000"
                    # Case for strange format, ex: 09-19-15-41 (month-day-hour-minute)
                    else:
                        #1) get month
                        now = datetime.datetime.now()
                        file_month = int(string_list[0])
                        if file_month > now.month:
                            file_year = now.year-1
                        else:
                            file_year = now.year
                        #2) if month is greater than now.month
                        #3) year = now.year || now.year-1
                        time_string = str(file_year) + "-" + string_list[0] + "-" + string_list[1] + " " + \
                                      string_list[2] + ":" + string_list[3].rstrip() + ":00.000"
                    timestamp = datetime.datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S.%f")
            elif "Serial Number" in value:
                sn = value.split(";")
                serial_num = sn[1]
            elif "Pulse Trend" in value:
                is_pulse = True
            elif is_pulse and "Trend Measurement" in value:
                position_line = value.split(";")
                position = position_line[3]     # get the position value
                list_of_positions.append(position)
                if "1" not in position_line[1]:
                    all_data_from_file.append(self.create_data_array(raw_data_list))
                    del raw_data_list[:]
            elif "Harmonic Phase" in value:
                params = value.split(";")
            elif len(value)>0 and (value[0].isdigit() or value[0] == '-'):
                raw_data_list.append(value)
            elif "END TREND" in value:
                pass
            else:
                pass

        # remove the time string from params list - it is not a parameter type
        del params[0]
        all_data_from_file.append(self.create_data_array(raw_data_list))
        del raw_data_list

        del file_name
        del is_pulse
        del number_of_buffer_points_skipped

        if len(position) == 0:
            list_of_positions.append("None")
        del position
        print("Finished the reading stage")
        return all_data_from_file, serial_num, params, timestamp, list_of_positions


    # get the chamber associated with the file
    def get_chamber(self, chamber_name, customer):
        chamber = None
        if Chamber.objects.filter(chamber_name=chamber_name, customer=customer).exists():
            chamber = Chamber.objects.get(chamber_name=chamber_name, customer=customer)
        del chamber_name
        del customer
        return chamber


    # get the sensor that generated the file
    def get_sensor(self, serial_num, chamber):
        sensor= None
        if Sensor.objects.filter(serial_number=serial_num, chamber=chamber).exists():
            sensor = Sensor.objects.get(serial_number=serial_num, chamber=chamber)
        del serial_num
        del chamber
        return sensor


    # get or create the data parameters that are present in the file
    def get_parameters(self, params, pulse_position, param_data, param_ids_from_file):
        for m in range(0, (len(params))):
            parameter_data = ParameterData(params[m], pulse_position)
            if parameter_data not in param_data:
                new_parameter = Parameter.objects.get_or_create(parameter_name=params[m], \
                                                                parameter_position=pulse_position, \
                                                                parameter_type="double")
                param_ids_from_file.append(new_parameter[0].id)
                param_data.append(parameter_data)
        return


    # create runs
    def create_runs(self, start_of_run, end_of_run, chamber, file, all_runs):
        if start_of_run is not None and end_of_run is not None:
            step_time = 0
            new_run = True
            # if overlapping with a run in all_runs, update the existing run
            for run in all_runs:
                if start_of_run >= run.start_time:
                    if start_of_run <= run.end_time:
                        new_run = False
                        if end_of_run > run.end_time:
                            # update run end_time
                            run.end_time = end_of_run
                        break
                elif end_of_run <= run.end_time:
                    if end_of_run >= run.start_time:
                        new_run = False
                        if start_of_run < run.start_time:
                            # update run start_time
                            run.start_time = start_of_run
                        break
            # if times do not overlap create a new run
            if new_run:
                r = Run(chamber=chamber, start_time=start_of_run, end_time=end_of_run, \
                         file=file, step_time=step_time)
                all_runs.append(r)
            start_of_run = None
            end_of_run = None
        return start_of_run, end_of_run

    # create data instances for all data contained in the row
    def create_row_data(self, param_ids_from_file, row_values, sensor, timestamp, all_data):
        for j, j_val in enumerate(param_ids_from_file):
            value = None
            try:
                # + 1 to compensate for time value in each row of data - time is not a parameter type
                value = float(row_values[j + 1])
            except:
                pass
            if value is not None:
                try:
                    val = Data(sensor=sensor, parameter_id=j_val, time=timestamp, \
                               parameter_value=value)
                    all_data.append(val)
                except:
                    pass
        return


    # write collected data (from readOctivFile()) to the database
    def write_data_to_db(self, read_data, chamber_name, customer_id, file):
        params = read_data[2]
        pulse_data_array = read_data[0]
        serial_num = read_data[1].strip(' \t\n\r')
        timestamp = read_data[3]
        pulses = read_data[4]
        customer = None
        #custCount = self.cursor.fetchall()
        if Customer.objects.filter(pk=customer_id).exists():
            customer = Customer.objects.get(pk=customer_id)
        else:
            print("No customer with this ID exists in the database.")
            return

        # get chamberID -------------------------------------------------------------------------
        chamber = self.get_chamber(chamber_name, customer)
        del customer
        if chamber == None:
            print("No Chamber")
            return
        chamber_id = chamber.pk
        # ---------------------------------------------------------------------------------------
        sensor = self.get_sensor(serial_num, chamber)
        del serial_num
        if sensor == None:
            print("No Sensor")
            return
        sensor_id = sensor.pk
        # ---------------------------------------------------------------------------------------
        # start writing data to the data table
        all_data = []
        all_runs = []

        # iterate through the data by pulse position it was collected at
        for pulse_num, rows_array in enumerate(pulse_data_array):
            param_data = []
            param_ids_from_file = []

            self.get_parameters(params, pulses[pulse_num], param_data, param_ids_from_file)

            start_of_run = None
            end_of_run = None
            end_of_file = datetime.timedelta(0, float(rows_array[(len(rows_array) - 1)][0]))
            time_at_end_of_file = timestamp + end_of_file

            if Data.objects.filter(sensor=sensor, parameter_id=param_ids_from_file[0], \
                                   time__gte=timestamp, time__lte=time_at_end_of_file).exists():
                print("Duplicate file")
                return
            # iterate through the rows of data generating data and run objects
            num_of_rows = len(rows_array)
            for k, var in enumerate(rows_array):
                if k%200 == 0:
                    print("Row: ", k, "/", num_of_rows)
                if float((var[4])) != 0 or float((var[2])) != 0:
                    timestamp2 = timestamp + datetime.timedelta(0, float((var[0])))
                    if start_of_run is None:
                        start_of_run = timestamp2
                    else:
                        end_of_run = timestamp2
                    self.create_row_data(param_ids_from_file, var, sensor, timestamp2, all_data)
                else:
                    start_of_run, end_of_run = self.create_runs(start_of_run, end_of_run, chamber, file, all_runs)
                if k == (len(rows_array) - 1):
                    start_of_run, end_of_run = self.create_runs(start_of_run, end_of_run, chamber, file, all_runs)

                # commit all of the data and run objects generated from the file
                if len(all_data) >= 8000:
                    start = time.time()
                    print("Writing to DB")
                    Data.objects.bulk_create(all_data, batch_size=999)
                    end = time.time()
                    print("DB writing done in " + str(end - start) + " seconds.")
                    del all_data[:]
        del chamber
        del params
        del pulses
        del pulse_data_array

        Data.objects.bulk_create(all_data, batch_size=999)
        del all_data
        Run.objects.bulk_create(all_runs, batch_size=999)
        del all_runs
        print("all data parsed")
        # mark the file as parsed
        file.parsed=True
        file.save(update_fields=['parsed'])
        return

    @task(name="File parser process")
    def process_file(self, file_dir, parse_file):
        start = time.time()
        file_data = self.read_octiv_file(file_dir)
        print("File read")
        self.write_data_to_db(read_data=file_data, chamber_name= \
                         parse_file.chamber.chamber_name, customer_id= \
                         parse_file.customer_id, file=parse_file)
        del file_data
        del file_dir
        del parse_file
        end = time.time()
        print("PARSED FILE, done in " + str(end - start) + " seconds.")
        return

