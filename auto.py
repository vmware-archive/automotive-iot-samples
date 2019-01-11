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

    def __init__(self, autoID, sensors_str):
        self.autoID = autoID
        sensors = clean_keys(sensors_str)   
        try :
            self.obd_conn = obd.OBD()
        except:
            print("Unexpected error: unable to connect to OBD", sys.exc_info()[0])
            self.obd_conn = None
        try :
            self.gps_conn = serial.Serial(constants.GPS_SERIAL, constants.GPS_BAUD_RATE, timeout=constants.SAMPLING_FREQUENCY)
        except:
            print("Unexpected error: unable to GPS", sys.exc_info()[0])
            self.gps_conn = None


    def is_connected(self):
        return self.obd_conn.is_connected()

    def get_sensors_str(self):
        return ",".join(self.keys)

    def read_sensors(self):
        """
        if an OBD connectio exists, it shall retrieve requested sensor data
        and return as a dictionary. 
        """
        data_dict = None 
        # read GPS
        # time and speed from GPS
        if gps_conn:
            line = gps_conn.readline()
            data_dict["GPS_TIME"] = 1234
            data_dict["GPS"] = ""
        # read OBD sensors
        if (self.obd_conn.is_connected()):
            for sensor in self.sensors:
                # appending results to row
                try:                 
                    val = str(conn.query(sensor).value.magnitude)
                except:
                    val = "Error"   
                data_dict[sensor] = val
        else:
            print("Unable to connect to obd sensors and read!!")  
        if data_dict : data_dict["TIME"] = time.time()  # from the compute device
        if (constants.DEBUG): print(data_dict)
        return data_dict
       
       

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
        self.total_distance_units += ispeed

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



    