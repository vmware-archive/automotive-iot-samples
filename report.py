import auto
import auto_domain
from config import config
import constants
import datetime
import json
import os
from pathlib import Path
import urllib.request
import requests
import time

def make_url(config_section):
    """ function that reads the specified configuration category related settings for protocol, IP address, port, and version
    to construct a url string
    params:
    config section: String  (example: "INSURANCE", "SMART_CITY", "MY_DRIVING")
    returns:
    url: String
    """
    url_str = config_section["PROTOCOL"] + "://" + config_section["ENDPOINT"] + ":" + str(config_section["PORT"]) + "/"
    version = config_section["VERSION"]
    if (version != "NULL"): 
        url_str = url_str + config_section["VERSION"] + "/"
    return url_str

 ## constants constructed from the configuration file.    

INSURANCE_URL = make_url(config["INSURANCE"])
SMART_CITY_URL = make_url(config["SMART_CITY"])
MY_DRIVING_URL = make_url(config["MY_DRIVING"])


# might we want to add vehicle data too?
def insurance_event_data(event_dict, autoID):
    """
    Assemble insurance event relevant data for transmission to insurance cloud endpoint
    params:
    event_dict which contains event_type, speed, gps-coordinates, and time information
    autoID: object that containers drivername, driverID, vehicle_model and vehicleID
    returns:
    a dictionary that captures all the information that an insurance event must contain per the insurance cloud endpoint
    """
    return {
        "client_side_id": autoID.driverID,
        "user": autoID.driverName, 
        "event_type": event_dict["EVENT_TYPE"],
        "event_timestamp": event_dict["TIME"] ,
        "gps_coord": event_dict["GPS"]
        }

# seems to be the same thing but the case of the keys is lower, and gps_coord (as opposed to GPS)
def smart_city_event_data(event_dict):
    """
    Assembles smart_city event relevant data for transmission to smart_city cloud endpoint
    params:
    event_dict which contains event_type, speed, gps-coordinates, and time information
    returns:
    a dictionary that captures all the information that an insurance event must contain per the insurance cloud endpoint
    """
    return {
            "event_type": event_dict["EVENT_TYPE"],
            "speed": event_dict["SPEED"],
            "event_timestamp": event_dict["TIME"] ,
            "gps_coord": event_dict["GPS"]
            }

def my_driving_event_data(date, distance, speedings, hard_breaks, places, autoID):
    """
    Assembles My_Driving event relevant event data  
    params:
    date, distance, number of speedings, number of hard breaks, places visited, 
    and AutoID object (contains driver and vehicle information)
    returns:
    a dictionary containing My_Driving relevant information.
    """
    return {
        "date": date,
        "client_side_id": autoID.driverID,
        "user": autoID.driverName, 
        "vehicle_model": autoID.vehicle_model,
        "vehicleID": autoID.vehicleID,
        "distance": distance,
        "speedings" : len(speedings), # perhaps we want the time and gps co-ordinates
        "hard_breaks": len(hard_breaks) ,# perhaps we want the time and gps co-ordinates
        "places": ",".join(places)
        }


def report_insurance_event(event_dict, autoID) :
    """
    Send insurance event to insurance cloud endpoint
    params:
    event_dict: event_type, speed, gps-coordinates, time
    autoID: object that containers drivername, driverID, vehicle_model and vehicleID
    returns:
    a dictionary that captures all the information that an insurance event must contain per the insurance cloud endpoint
    """
    data_json = json.dumps(insurance_event_data(event_dict, autoID))
    headers = {'Content-type': 'application/json'}
    url = INSURANCE_URL + "add_event"
    response = requests.post(url, data=data_json, headers=headers)
    if constants.DEBUG:
        print("*********** Insurance Reporting  " + event_dict["EVENT_TYPE"] )
        print(response.status_code)


def report_smart_city_event(event_dict):
    """
    Send Smart_City  event to Smart_City  cloud endpoint
    params:
    event_dict  (contains event_type, speed, gps-coordinates, time information)
    returns:
    a dictionary that captures all the information that a smart_city event must contain per the insurance cloud endpoint
    """
    data_json = json.dumps(smart_city_event_data(event_dict))
    headers = {'Content-type': 'application/json'}
    url = SMART_CITY_URL + "add_event"
    response = requests.post(url, data=data_json, headers=headers)
    if constants.DEBUG:
        print("*********** Smart City Reporting  " + event_dict["EVENT_TYPE"])
        print(response.status_code)


def report_my_drive_event(date, distance, speedings, hard_breaks, places, autoID):
    data = my_driving_event_data(date, distance, speedings, hard_breaks, places, autoID)
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json'}
    url = MY_DRIVING_URL + "add_event"
    response = requests.post(url, data=data_json, headers=headers)
    if constants.DEBUG:
        print("*********** Reporting My Driving Report")
        print(response.status_code)

def report_event(event_dict, autoID):
    event_type = event_dict["EVENT_TYPE"]
    if (constants.INSURANCE_ENABLED and (event_type in constants.INSURANCE_EVENTS)):
        print("Found a " + event_type + " to report!!!")
        report_insurance_event(event_dict, autoID)
    if constants.SMART_CITY_ENABLED:
        report_smart_city_event(event_dict)


def report_all_events():
    """
    Processes all events recorded in events log file iteratively.
    Based on event type and enabled cloud endpoints, events are reported.
    Slow-down events are reported only to smart city, and no driver or vehicle ID data is shared with smart city.
    Only a single event is transmitted at the end of drive ssion to the My Driving endpoint
    """

    autoID = auto.AutoID(constants.DRIVER_NAME, constants.DRIVER_ID, constants.VEHICLE_MODEL, constants.VEHICLE_ID)   
    print("The driver is " + autoID.driverID)
    drive = auto.Drive(autoID,constants.SAMPLING_FREQUENCY, constants.HISTORY)
    places = "Paris, Timbucktoo"
    distance = auto_domain.get_distance()
 
    with open(constants.EVENTS_FILENAME,'r') as file:
        for cnt, event_str in enumerate(file):
            print(str(cnt) + "  " + event_str)
            event_dict = auto_domain.get_event_dict(event_str)
            report_event(event_dict, autoID)
            if constants.MY_DRIVING_ENABLED:
                drive.update_events(event_dict)
                      
    if constants.MY_DRIVING_ENABLED:
        report_my_drive_event(datetime.date.today(), distance, len(drive.speedings), len(drive.hard_breaks), places, autoID)


def test():
    """
    Test payload transmission to insurance cloud endpoint
    """
    autoID = auto.AutoID("a", "b", "c", "d")
    event_dict = { "TIME" : 123456,
                   "EVENT_TYPE": "hard_break",
                   "SPEED" : 85,
                   "GPS" : "31.5, 41.5"
                 }
    report_insurance_event(event_dict, autoID) 


# do we have connectivity?!
def main():
    """
    Reports all events saved in events log file to enabled cloud endpoints:
    Insurance
    Smart City and
    My Driving
    The assumption is that durig driving no internet access is available.
    Thus events saved to an events log file.
    """

    test()
    if Path(constants.EVENTS_FILENAME).is_file():
        successful = False
        while (not successful):
            try:
                urllib.request.urlopen("http://www.google.com") 
                #urllib.request.urlopen("http://www.nowhere.com") # nowhere!
                report_all_events()
                successful = True
                os.rename(constants.EVENTS_FILENAME, constants.EVENTS_FILENAME_BACKUP)
                if Path(constants.DISTANCE_TRAVELED_FILENAME).is_file():
                    os.rename(constants.DISTANCE_TRAVELED_FILENAME, 
                        constants.DISTANCE_TRAVELED_FILENAME_BACKUP)
            except:
                time.sleep(constants.REPORT_RETRY_SEC)
                #keep trying!  
               



if __name__ == "__main__":
    # execute only if run as a script
    main()