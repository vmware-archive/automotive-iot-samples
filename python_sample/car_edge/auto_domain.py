from config import config
import constants
from pathlib import Path
import os

# TODO 
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


#https://copradar.com/chapts/references/acceleration.html
#http://tracknet.accountsupport.com/wp-content/uploads/Verizon/Hard-Brake-Hard-Acceleration.pdf
## My lack of knowledge, does the drop happen over a second or over milliseconds?
## should one take the min time and max time across the buffer and the min speed and max speed? 
def check_for_events_of_interest(data_buffer):
    
    max_speed = -1
    min_speed = 1000000
    max_speed_datum = None
    min_speed_datum = None

    for i in range(0, data_buffer.capacity()):
        curr = data_buffer[i]
        if curr:
            curr_speed = curr[OBD]["SPEED"]
            if (curr_speed > max_speed):
                max_speed_datum = curr
                max_speed = curr_speed
            if (curr_speed < min_speed):
                min_speed = curr_speed
                min_speed_datum = curr

    # time order data
    if max_speed_datum:
        if (max_speed_datum["TIME"] > min_speed_datum["TIME"]):
            begin = min_speed_datum
            end = max_speed_datum
        else :
            begin = max_speed_datum
            end = min_speed_datum
     
        # time in milliseconds
        time_interval = end["TIME"] - begin["TIME"]
        speed_change = end["OBD"]["SPEED"] - begin["OBD"]["SPEED"]

        # to obtain acceleration/deceleration in  miles/hour/second
        speed_rate_of_change = (speed_change/time_interval) * 1000
        if (speed_rate_of_change > HEAVY_HARD_ACC):
            return constants.HARD_ACC
        elif (speed_ratechange < HEAVY_BREAK):
            return constants.HARD_BREAK
        elif speeding(max_speed, max_speed_datum["GPS"]):
            return constants.SPEEDING
    #default
    return constants.NORMAL



def speeding(speed, gps):  
    """
    Returns true if current speed is above speed limit at given GPS coordinates
    """
    
    return (speed > get_speed_limit(gps)) 




def log_auto_event (event_type, data_dict):
    event_str = data_dict["TIME"] + "," \
                + event_type +  "," \
                + data_dict["SPEED"] +  "," \
                + data_dict.setdefault("GPS", constants.DEFAULT_GPS)
    with open(constants.EVENTS_FILENAME, 'a') as file:
        file.write(event_str + "\n")

def get_event_dict (event_str):
    details = event_str.split(",")
    return {
        "TIME": details[0],
        "EVENT_TYPE": details[1],
        "SPEED": details[2],
        "GPS": details[3] + "," + details[4]
    }

def distance_traveled(distance_units):
    # sampling frequency in seconds
    # speed provided in kilometers or miles per hour
    # need to convert sampling frequency to hours
    actual_distance = distance_units *  constants.SAMPLING_FREQUENCY  * (1.0/3600)
    print(str(actual_distance) + constants.DISTANCE_UNITS_LABEL)
    return str(actual_distance) + constants.DISTANCE_UNITS_LABEL

    
def log_distance(distance_units):
    filename = constants.DISTANCE_TRAVELED_FILENAME
    if Path(filename).is_file():
        # rename it -- just in case system crashes we do not lose all data
        os.rename(filename, constants.DISTANCE_TRAVELED_FILENAME_BACKUP)

    # the frequency at which we take readings times the unit
    # say we examine every minute and are driving at 30 miles/hr, in one minute a distance of 0.5 miles covered
    with open(filename, 'w') as file:
        file.write(distance_traveled(distance_units))

# do we not want the units?
# do we want return value to be an integer?
def get_distance():
    filename = constants.DISTANCE_TRAVELED_FILENAME
    if Path(filename).is_file():
        with open(filename, 'r') as file:
            distance_str = file.read()
        os.rename(filename, constants.DISTANCE_TRAVELED_FILENAME_BACKUP)
    else:
        return distance_traveled(0)
