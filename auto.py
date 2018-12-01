from config import config
import constants
import obd
import serial
import time


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
    obd_connection = None
    sensors = []

    def __init__(self, autoID, sensors_str):
        self.autoID = autoID
        sensors = clean_keys(sensors_str)   
        try :
            self.obd_connection = obd.OBD()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            self.obd_connection = Null


    def is_connected(self):
        return self.obd_connection.is_connected()

    def get_sensors_str(self):
        return ",".join(self.keys)

    def read_sensors(self):
        """
        if an OBD connectio exists, it shall retrieve requested sensor data
        and return as a dictionary. 
        """
        data_dict = None
        if (self.obd_connection.is_connected()):
            data_dict = {"TIME": time.time()}
            for sensor in self.sensors:
                # appending results to row
                try:
                    # TODO GPS implementation
                    val = None
                    if (sensor == "GPS") :  
                        val = constants.DEFAULT_GPS
                    else:
                        val = str(connection.query(sensor).value.magnitude)
                except:
                    val = "Error"   
                data_dict[sensor] = val
            if (constants.DEBUG):
                print(data_dict)
            return data_dict
        else:
            print("Unable to connect to obd sensors and read!!") 
            return None
       

# add locks for later multithread programming
class RingBuffer:
    capacity = 0
    curr = 0
    data = []

    def __init__(self, capacity) :
        self.capacity = capacity


    def add_element(self, datum) :
        next_ele = (self.curr + 1)
        if (next_ele < self.capacity):
            self.data.append(datum)
        else:
            next_ele = next_ele % self.capacity
            self.data[next_ele] = datum
        self.curr = next_ele

    def accelerations(self):
        accelerations = []
        val = self.data[self.curr]
        for i in range(1, self.capacity): 
            next = (self.curr - i) % self.capacity
            next_val = self.data[next]
            accelerations.append(val - next_val)
            val = next_val
        return accelerations


class Drive():
    # is an object that captures details such as driver name, id, vehicle model and id
    autoID = None
    # ringbuffer of fixed capacity
    data_buffer = None
    # float, represents how frequently the sensors are polled
    time_unit = 0 
    # a running sum of distance traveled as an integer, based on speed in
    # kms/hr or miles/hr
    total_distance_units = 0 
    # last time the distance traveled information was saved to some persistence store
    last_save_time = 0

    speedings = []
    hard_breaks = []
    slow_downs = []
    
    def __init__(self, autoID, time_unit, history): 
        self.autoID = autoID
        self.time_unit = time_unit  
        self.data_buffer = RingBuffer(history) 
        self.last_save_time = time.time()

    
    def save_time(self):
        retval = False
        now = time.time()  # time since epoch in seconds as a float
        if ((now - self.last_save_time) > constants.SAVE_LOCAL_SEC):
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



    