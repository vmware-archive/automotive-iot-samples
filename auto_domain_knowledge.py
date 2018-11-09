import json
import requests
import time
from config import config

class OBD_parser():
    # comma separated field headings string
    field_headings = ""
    keys = []

    def __init__(self, field_headings):
        self.field_headings = field_headings
        self.keys = field_headings.split(",")
    
    def parse_data(self, data_str):
        values = data_str.split(",")
        return dict(zip(self.keys, values))

   


# add locks for later multithread programming
class Ring_Buffer:
    capacity = config["EDGE"]["RING_BUFFER_CAPACITY"] 
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


        
def make_url(config_section):
    url_str = config_section["PROTOCOL"] + "://" + config_section["ENDPOINT"] + ":" + str(config_section["PORT"]) + "/"
    if (config_section["VERSION"] != ""): 
        url_str = url_str + config_section["VERSION"] + "/"
    return url_str

#########################
###
### OBJECTS
#########################
CAR_DATA_PARSER = OBD_parser("TIME, SPEED, GPS")
DATA_BUFFER = Ring_Buffer(5)


INSURANCE_URL = make_url(config["INSURANCE"])
SMART_CITY_URL = make_url(config["SMART_CITY"])
MY_DRIVING_URL = make_url(config["MY_DRIVING"])
CAR_DATA_FILE = config["EDGE"]["DEVICE_DATA_FILE"]

DRIVER_NAME = config["DEVICE"]["Driver"]
VEHICLE_ID = config["DEVICE"]["VehicleID"]
DEBUG = config["COMMON"]["DEBUG"]

def get_speed_limit(gps) :
    """
    # TODO determine speeding threshold based on gps co-ordinates
    https://developers.google.com/maps/documentation/roads/speed-limits
     if we do not have constant connectivity .. would need to make these API calls back where we have connectivity
     also does not make sense to call for each recorded location!
     scalability/performance etc is in the details such as this!!
    """
    #ignore gps for now
    return 70


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
        print("Reporting speeding " )
        print(response.status_code)
    return

def stream_data(sensor_data_str):
    # write it to circular buffer
    data_dict = CAR_DATA_PARSER.parse_data(sensor_data_str)

    ## TODO .. make processing of the ring buffer happen at some periodicity in a separate thread
    ## use locks, one producer, one consumer
    timestamp = data_dict["TIME"]
    speed = data_dict["SPEED"]
    DATA_BUFFER.add_element(speed)
    gps = "37.7992520359445,-122.41955459117891"

    # TODO -- use the full data_buffer
    if is_speeding(speed, gps):
        report_speeding(speed, gps, timestamp)