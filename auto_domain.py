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

# TODO 
#https://copradar.com/chapts/references/acceleration.html
#http://tracknet.accountsupport.com/wp-content/uploads/Verizon/Hard-Brake-Hard-Acceleration.pdf
def is_hard_break(edge):
    return False
    

def is_speeding(speed, gps):  
    """
    Returns true if current speed is above speed limit at given GPS coordinates
    """
    
    return (speed > get_speed_limit(gps)) 


# TODO -- to actually do something intelligent with the data
# does python have an enumneration type?
def get_event_type(drive, data_dict):
    event_type = constants.NORMAL
    speed = int(data_dict["SPEED"])
    gps = data_dict.setdefault("GPS", constants.DEFAULT_GPS)
    if (speed < 0):
        event_type = constants.HARD_BREAK
    elif (speed < 5):
        event_type = constants.SLOW_DOWN
    elif (speed > 50):
        event_type = constants.SPEEDING
    return event_type



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
    filename = constants.DISTANCE_FILENAME
    if Path(filename).is_file():
        with open(filename, 'r') as file:
            distance_str = file.read()
        os.rename(filename, constants.DISTANCE_FILENAME_BACKUP)
    else:
        return distance_traveled(0)
