import json
import requests
import time
from config import config
import obd
import serial


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


class Data_Parser():
    sensors_str = ""
    keys = []

    def __init__(self, sensors_str):
        self.sensors_str = sensors_str
        pre_keys = sensors_str.split(",")
        for key in pre_keys:
            if (key != ""):
                self.keys.append(key.strip())

    def get_dict(self, data_str):
        values = data_str.split(",")
        return dict(zip(self.keys, values))


          
class Automobile():
    data_parser = None
    obd_connection = None
    cmd_list = []

    def __init__(self, sensors_str):
        self.data_parser = Data_Parser(sensors_str) 
        for key in self.data_parser.keys:
            self.cmd_list.append(SENSOR_CMDS[key])    
        # self.obd_connection = obd.OBD()

    def get_sensors_str(self):
        return self.data_parser.sensors_str

    def read_sensors(self):
        if (self.obd_connection is not None):
            line_text = str(time.time()) + ", " #new row with time 
            for cmd in self.cmd_list:
                # appending results to row
                try:
                    # TODO add GPS co-ordinates too .. else we shall need to track a separate file and
                    # match up data based on time stamp
                    line_text += str(connection.query(cmd).value.magnitude) + ", "
                except:
                    line_text +=  "Error, "
                    print("Unexpected error:", sys.exc_info()[0])
            return line_text
        else:
            print("No sensors to read!!!")
            return ""



# add locks for later multithread programming
class Ring_Buffer:
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


class Edge:
    data_parser = None
    data_buffer = None

    def __init__(self, sensors_str): 
        self.data_parser = Data_Parser(sensors_str)  
        self.data_buffer = Ring_Buffer(int(config["EDGE"]["RING_BUFFER_CAPACITY"]))
        if DEBUG:
            print(self.data_parser.keys)
        

    def process_stream_data(self, sensor_data_str):
        # write it to circular buffer
        data_dict = self.data_parser.get_dict(sensor_data_str)
        if (DEBUG):
            print(data_dict)

        ## TODO .. make processing of the ring buffer happen at some periodicity in a separate thread
        ## use locks, one producer, one consumer
        timestamp = int(data_dict["TIME"])
        speed = int(data_dict["SPEED"])
        self.data_buffer.add_element(speed)
        gps = "37.7992520359445,-122.41955459117891"

        # TODO -- use the full data_buffer
        if is_speeding(speed, gps):
            report_speeding(speed, gps, timestamp)


def make_url(config_section):
    url_str = config_section["PROTOCOL"] + "://" + config_section["ENDPOINT"] + ":" + str(config_section["PORT"]) + "/"
    version = config_section["VERSION"]
    if (version != "NULL"): 
        url_str = url_str + config_section["VERSION"] + "/"
    return url_str


#########################
###
### OBJECTS
#########################

DATA_BUFFER = Ring_Buffer(5)
AUTOMOBILE = None

INSURANCE_URL = make_url(config["INSURANCE"])
SMART_CITY_URL = make_url(config["SMART_CITY"])
MY_DRIVING_URL = make_url(config["MY_DRIVING"])

DRIVER_NAME = config["DEVICE"]["Driver"]
VEHICLE_ID = config["DEVICE"]["VehicleID"]


def get_speed_limit(gps) :
    """
    # TODO determine speeding threshold based on gps co-ordinates
    https://developers.google.com/maps/documentation/roads/speed-limits
     if we do not have constant connectivity .. would need to make these API calls back where we have connectivity
     also does not make sense to call for each recorded location!
     scalability/performance etc is in the details such as this!!
    """
    #ignore gps for now
    return 50


def is_speeding(speed, gps):
    """
    Returns true if current speed is above speed limit at given GPS coordinates
    """
    
    return (speed > get_speed_limit(gps)) 

def report_speeding(speed, gps, timestamp):
    """
    Send SPEEDING event to cloud endpoint
    """
    # curl -d '{"message":"Hello World!"}' -H "Content-Type: application/json" -X POST http://localhost:2000/post_example

    data = {
    "client_side_id": VEHICLE_ID, 
    "user": DRIVER_NAME, 
    "event_type": "SPEEDING", 
    "event_timestamp": time.time(), 
    # "gps_coord": "37.7992520359445,-122.41955459117891"
    "gps_coord": gps
    }
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json'}

    url = INSURANCE_URL + "add_event"
    
    response = requests.post(url, data=data_json, headers=headers)

    if DEBUG:
        print("***********Reporting speeding " )
        print(response.status_code)
    return

    AUTOMOBILE = None




    