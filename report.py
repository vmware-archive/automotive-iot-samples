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
    url_str = config_section["PROTOCOL"] + "://" + config_section["ENDPOINT"] + ":" + str(config_section["PORT"]) + "/"
    version = config_section["VERSION"]
    if (version != "NULL"): 
        url_str = url_str + config_section["VERSION"] + "/"
    return url_str

INSURANCE_URL = make_url(config["INSURANCE"])
SMART_CITY_URL = make_url(config["SMART_CITY"])
MY_DRIVING_URL = make_url(config["MY_DRIVING"])


# might we want to add vehicle data too?
def insurance_event_data(event_dict, autoID):
    return {
        "client_side_id": autoID.driverID,
        "user": autoID.driverName, 
        "event_type": event_dict["EVENT_TYPE"],
        "event_timestamp": event_dict["TIME"] ,
        "gps_coord": event_dict["GPS"]
        }

# seems to be the same thing but the case of the keys is lower, and gps_coord (as opposed to GPS)
def smart_city_event_data(event_dict):
    return {
            "event_type": event_dict["EVENT_TYPE"],
            "speed": event_dict["SPEED"],
            "event_timestamp": event_dict["TIME"] ,
            "gps_coord": event_dict["GPS"]
            }

def my_driving_event_data(date, distance, speedings, hard_breaks, places, autoID):
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
        Send insurance event to cloud endpoint
    """
    data_json = json.dumps(insurance_event_data(event_dict, autoID))
    headers = {'Content-type': 'application/json'}
    url = INSURANCE_URL + "add_event"
    response = requests.post(url, data=data_json, headers=headers)
    if constants.DEBUG:
        print("*********** Insurance Reporting  " + event_dict["EVENT_TYPE"] )
        print(response.status_code)


def report_smart_city_event(event_dict) :
    data_json = json.dumps(auto_domain.smart_city_event(event_dict))
    headers = {'Content-type': 'application/json'}
    url = SMART_CITY_URL + "add_event"
    response = requests.post(url, data=data_json, headers=headers)
    if constants.DEBUG:
        print("*********** Smart City Reporting  "+ event_type )
        print(response.status_code)


def report_my_drive_event(date, distance, speedings, hard_breaks, places, autoID):
    data = auto_domain.my_driving_event_data(date, distance, speedings, hard_breaks, places)
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json'}
    url = MY_DRIVING_URL + "add_event"
    response = requests.post(url, data=data_json, headers=headers)
    if constants.DEBUG:
        print("*********** My Driving Reporting  "+ event_type )
        print(response.status_code)

def report_event(event_dict, autoID): 
    event_type = event_dict["EVENT_TYPE"]
    if (constants.INSURANCE_ENABLED and (event_type in constants.INSURANCE_EVENTS)):
        print("Found a " + event_type + " to report!!!")
        report_insurance_event(event_dict, autoID)
    if constants.SMART_CITY_ENABLED:
        report_smart_city_event(event_dict, autoID)



def report_all_events():
    autoID = auto.AutoID(constants.DRIVER_NAME, constants.DRIVER_ID, constants.VEHICLE_MODEL, constants.VEHICLE_ID)   
    print("The driver is " + autoID.driverID)
    drive = auto.Drive(autoID,constants.SAMPLING_FREQUENCY, constants.HISTORY)
    places = "Paris, Timbucktoo"
    distance = auto_domain.get_distance()

    
    with open(constants.EVENTS_FILENAME,'r') as file:
        for cnt, event_str in enumerate(file):
            print(str(cnt) + "  " + event_str)
            event_dict = auto_domain.get_event_dict(event_str)
            event_type = event_dict["EVENT_TYPE"]
            report_event(event_dict, autoID) 
            if constants.MY_DRIVING_ENABLED:
                drive.update_events(event_dict)
                report_event(event_dict, autoID)         
    if constants.MY_DRIVING_ENABLED:
        report_my_drive_event(datetime.date.today(), distance, num_speedings, num_hard_breaks, places, autoID)


def test():
    autoID = auto.AutoID("a", "b", "c", "d")
    event_dict = { "TIME" : 123456,
                   "EVENT_TYPE": "hard_break",
                   "SPEED" : 85,
                   "GPS" : "31.5, 41.5"
                 }
    report_insurance_event(event_dict, autoID) 


# do we have connectivity?!
def main():
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
                if Path(constants.DISTANCE_FILENAME).is_file():
                    os.rename(constants.DISTANCE_FILENAME, constants.DISTANCE_FILENAME_BACKUP)
            except:
                time.sleep(constants.REPORT_RETRY_SEC)
                #keep trying!  
               



if __name__ == "__main__":
    # execute only if run as a script
    main()