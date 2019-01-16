from config import config
import constants
import obd
import serial
import time
import sys


DEBUG = config["COMMON"]["DEBUG"]

SENSOR_CMDS = { 
    "TIME" : "skip",
    "SPEED" : obd.commands.SPEED,
    "RPM" : obd.commands.RPM,
    "FUEL_LEVEL" : obd.commands.FUEL_LEVEL,
    "RELATIVE_ACCEL_POS" : obd.commands.RELATIVE_ACCEL_POS,
    "ABSOLUTE_LOAD" : obd.commands.ABSOLUTE_LOAD,
    "ENGINE_LOAD" : obd.commands.ENGINE_LOAD,
    "RELATIVE_THROTTLE_POS" : obd.commands.RELATIVE_THROTTLE_POS,
    "THROTTLE_POS_B" : obd.commands.THROTTLE_POS_B,
    "THROTTLE_POS_C" : obd.commands.THROTTLE_POS_C
}

GPS_METRICS = [
    'fix_time',
    'validity',
    'latitude',
    'latitude_hemisphere' ,
    'longitude' ,
    'longitude_hemisphere' ,
    'speed',
    'true_course',
    'fix_date',
    'variation',
    'variation_e_w',
    'checksum',
    'decimal_latitude',
    'decimal_longitude'
    ]

class AutoID () :
    driverName = "Someone"
    driverID = "1234"
    vehicleModel = "E24 M6 BMW"
    vehicleID= "some_vehicle"

    def __init__(self, driverName, driverID, vehicleModel, vehicleID):
        self.driverName = driverName
        self.driverID = driverID
        self.vehicleModel = vehicleModel
        self.vehicleID = vehicleID


def clean_keys(keys_str):
    pre_keys = keys_str.split(",")
    keys = []
    for key in pre_keys:
        if (key != ""):
            keys.append(key.strip())
    return keys


class DataParser():
    sensors_str = None
    keys = None

    def __init__(self, sensors_str):
        self.sensors_str = sensors_str
        self.keys = clean_keys(sensors_str)
        print( self.keys)

    def parse(self, data_str):
        if (constants.DEBUG):
            print("Data str to be parsed: " + data_str)
        values = data_str.split(",")
        if (constants.DEBUG):
            print(values)
        return dict(zip(self.keys, values))


          
class Automobile():
    autoID = None
    obd_conn = None
    gps_conn = None
    sensors = []
    sensors_connections = []
    metrics = {}

    def __init__(self, autoID, sensors):
        self.autoID = autoID
        self.sensors = sensors
        self.metrics = None

        if "OBD" in self.sensors:
            try :
                self.obd_conn = obd.OBD()
                if self.obd_conn.status() != "Not Connected":
                    self.sensors_connections.append(self.obd_conn)
            except:
                print("Unexpected error: unable to connect to OBD", sys.exc_info()[0])
                self.obd_conn = None
        
        if "GPS" in self.sensors:
            for i in range(11):
                try :
                    print("Trying top connect to GPS on serial /dev/ttyUSB" + str(i))
                    self.gps_conn = serial.Serial("/dev/ttyUSB" + str(i), constants.GPS_BAUD_RATE, timeout=constants.SAMPLING_FREQUENCY)
                    self.sensors_connections.append(self.gps_conn)
                    print("Connected to serial /dev/ttyUSB" + str(i))
                    break
                except:
                    print("Unexpected error: unable to GPS", sys.exc_info()[0])
                    self.gps_conn = None
        

    def get_tracked_metrics(self):
        """
        Returns list of tracked metrics according to connected sensors
        and metrics supported by car (for OBD)
        """
        metric_list = []

        if self.gps_conn:
            metric_list += GPS_METRICS
        if self.obd_conn:
            metric_list += SENSOR_CMDS.keys()

        # Returns None if no connection was made
        if not self.gps_conn and not self.obd_conn:
            return None
        
        return metric_list


    def read_sensors(self):
        """
        if OBD or GPS connection exist, it shall retrieve requested sensor data
        and return as a dictionary. 
        """
        data_dict = None
        #########
        # GPS
        #########
        if self.gps_conn:
            data_dict = {}
            line = ""
            # Reading lines from serial until GPRMC arrives
            while line == "":
                temp_line = str(self.gps_conn.readline())
                if "$GPRMC" in temp_line:
                    # found GPRMC line. Recording it.
                    line = temp_line
                    GPS_data = self.parse_gps_data(line)
                    if not data_dict:
                        data_dict = GPS_data
        else:
            print("Unable to connect to gps sensors and read!!")  
        

        #########
        # OBD
        #########
        if (self.obd_conn.is_connected()):
            if not data_dict:
                data_dict = {}
            for key in SENSOR_CMDS:
                # appending results to row
                try:
                    val = str(self.obd_conn.query(SENSOR_CMDS[key]).value.magnitude)
                except:
                    val = "Error"   
                data_dict[key] = val
        else:
            print("Unable to connect to obd sensors and read!!")  

        if data_dict :
            data_dict["TIME"] = time.time()  # from the compute device
            
        if (constants.DEBUG): 
            print(data_dict)
        
        return data_dict
    
    def parse_gps_data(self, GPS_data_line):
        """
        Input: line read from GPS serial
        output: dictionary containing all formatted data points

        Time and data are converted from hhmmss.ss and ddmmyy format to unix timestamp.

        Lat and lon coordinates are converted from degrees 
        and hemisphere (E - W or N - S) to decimal format 
        (positive for N and E and negative for S and W)

        Code inspired from script found at:
        https://github.com/mrichardson23/gps_experimentation/blob/master/gps.py 
        """
        line_split = GPS_data_line.split(",")

        GPS_data_point = {
            'fix_time': line_split[1],
            'validity': line_split[2],
            'latitude': line_split[3],
            'latitude_hemisphere' : line_split[4],
            'longitude' : line_split[5],
            'longitude_hemisphere' : line_split[6],
            'speed': line_split[7],
            'true_course': line_split[8],
            'fix_date': line_split[9],
            'variation': line_split[10],
            'variation_e_w' : line_split[11],
            'checksum' : line_split[12]
        }
    
        GPS_data_point['decimal_latitude'] = self.degrees_to_decimal(GPS_data_point['latitude'], GPS_data_point['latitude_hemisphere'])
        GPS_data_point['decimal_longitude'] = self.degrees_to_decimal(GPS_data_point['longitude'], GPS_data_point['longitude_hemisphere'])

        # TODO: convert time and date from hhmmss.ss and ddmmyy to timestamp

        return GPS_data_point

    def degrees_to_decimal(self, data, hemisphere):
        """
        Converts gps output coord from degree to decimal.
        """
        try:
            decimalPointPosition = data.index('.')
            degrees = float(data[:decimalPointPosition-2])
            minutes = float(data[decimalPointPosition-2:])/60
            output = degrees + minutes
            if hemisphere is 'N' or hemisphere is 'E':
                return output
            if hemisphere is 'S' or hemisphere is 'W':
                return -output
        except:
            return ""

    

# add locks for later multithread programming
class RingBuffer:
    capacity = 0
    curr = -1
    data = []

    def __init__(self, capacity) :
        self.capacity = capacity
        self.curr = -1
        for i in range(0, capacity):
            self.data.append(None)

    def add(self, datum) :   
        next = (self.curr + 1) % self.capacity
        self.data[next] = datum
        self.curr = next
 


class Drive():
    # is an object that captures details such as driver name, id, vehicle model and id
    autoID = None
    analysis_window = constants.HISTORY
    # ringbuffer of fixed capacity
    data_buffer = None
    # float, represents how frequently the sensors are polled
    time_unit = 0 
    # a running sum of distance traveled as an integer, based on speed in
    # kms/hr or miles/hr
    total_distance_units = 0 
    # last time the distance traveled information was saved to some persistence store
    last_save_time = 0
    # peridically save the data locally to protect from connectivity issues, crashes, power-off
    save_interval= -1 
    
    sample = 0
    speedings = []
    hard_breaks = []
    slow_downs = []
    
    def __init__(self, autoID, time_unit, data_buffer_size, save_interval): 
        self.autoID = autoID
        self.data_buffer_size = data_buffer_size
        self.analysis_window_size = data_buffer_size % 2
        self.data_buffer = RingBuffer(data_buffer_size) 
        self.save_interval = save_interval
        self.last_save_time = time.time()

    def analysis_time(self):
        if self.analysis_window_size == 0:
            return False
        return ((self.sample % self.analysis_window_size) == 0)

    
    def inc_samples(self):
        self.sample = (self.sample + 1) % constants.MAX_READINGS # prevents overflow

    # a helper method to determine based on configured parameters whether to persist data locally
    def save_time(self):
        retval = False
        if (self.save_interval > -1.0):
            now = time.time()  # time since epoch in seconds as a float
            if ((now - self.last_save_time) > self.save_interval):
                self.last_save_time = now
                retval = True
                print("save distance now = " + str(retval))
        return retval

    # for efficiency will deal with the time multiplier when consuming this value elsewhere
    def update_distance(self,ispeed):
        self.total_distance_units += float(ispeed)

    def update_events(self, event_dict):
        event_type = event_dict["EVENT_TYPE"]
        if (event_type == constants.SPEEDING):
            self.speedings.append(event_dict)
        elif (event_type == constants.HARD_BREAK):
            self.hard_breaks.append(event_dict)
        elif (event_type == constants.SLOW_DOWN):
            self.slow_downs.append(event_dict)
        else:
            pass



    