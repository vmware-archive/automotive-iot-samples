from config import config
from auto import AutoID, Automobile, DataParser, Drive
import auto_domain 
import constants
from report import report_event
from pathlib import Path
import sys
import time



def process_stream_data(drive, data_dict):
    speed = int(data_dict["SPEED"])
    drive.data_buffer.add_element(speed)
    drive.update_distance(speed)
    # periodically persist the distance traveled, so as not to lose all the data should the device reboot/power-off
    if drive.save_time():
        auto_domain.log_distance(drive.total_distance_unit)

    event_type = auto_domain.get_event_type(drive, data_dict)
    if not (event_type == constants.NORMAL):
        data_dict["EVENT_TYPE"] = event_type  # data_dict enhanced with event_type 
        auto_domain.log_auto_event(event_type, data_dict)  
        drive.update_events(data_dict)
        if constants.STREAM:
            report_event(data_dict, drive.autoID)
    

# Read the pre-recorded data and process each item as if live-streamed
# thus the call to process_stream_data
def process_recorded_data():
    print("Reading pre-recorded data from: " + constants.DATA_FILENAME)
    if Path(constants.DATA_FILENAME).is_file():
        with open(constants.DATA_FILENAME, "r", encoding='utf-8-sig') as file :
            try:
                # first line contains table headers, indicates contents
                #sensors_str = "TIME, SPEED, RPM, FUEL_LEVEL, ABSOLUTE_LOAD, ENGINE_LOAD, RELATIVE_THROTTLE_POS, THROTTLE_POS_B" 
                sensors_str = file.readline()
                if constants.DEBUG:
                    print("Data file headings  = " + sensors_str)
                if (sensors_str != "") :
                    data_parser = DataParser(sensors_str)
                    print("Data parser constructed")
                    autoID =  AutoID(constants.DRIVER_NAME, constants.DRIVER_ID, constants.VEHICLE_MODEL, constants.VEHICLE_ID)
                    print("autoID constructed")
                    print("the driverID = " + autoID.driverID)
                    drive = Drive(autoID,constants.SAMPLING_FREQUENCY, constants.HISTORY, constants.SAVE_INTERVAL_LOCAL)
                    for cnt, data_line in enumerate(file):
                        if constants.DEBUG:
                            print(data_line)
                        data_dict = data_parser.parse(data_line)
                        if data_dict:
                            process_stream_data(drive, data_dict)
                        else:
                            print("Data recording in incorrect format!") 
                else:
                    print("No data parser to process the pre-recorded data")
            except:
                print("Unexpected error:", sys.exc_info()[0])
    else:
        print("No car data to process! Bye!")


def record_sensor_headings():
    with open(constants.DATA_FILENAME, 'w') as file:
        file.write(constants.SENSORS)

def record_sensor_readings(data_dict):
    sensor_vals = []
    for key, val in data_dict.items():
        sensor_vals.append(str(val))
    vals =  ",".join(sensor_vals)
    with open(constants.DATA_FILENAME, 'w') as file:
        file.write(vals)
   

def process_live_data():
    autoID =  AutoID(constants.DRIVER_NAME, constants.DRIVER_ID, constants.VEHICLE_MODEL, constants.VEHICLE_ID)
    automobile = Automobile(autoID, constants.SENSORS)
    if not automobile.is_connected():
        print("Unable to connect to automobile sensors. \nBye!")

    drive = Drive(autoID, constants.SAMPLING_FREQUENCY, constants.HISTORY, constants.SAVE_INTERVAL_LOCAL)
    if constants.RECORD:
            record_sensor_headings()

    while automobile.is_connected():
        # reads the data from the various sensors
        data_dict = automobile.read_sensors()
        if data_dict:
            process_stream_data(drive, data_dict) 
        if constants.RECORD:
            record_sensor_readings(data_dict)

        time.sleep(constants.SAMPLING_FREQUENCY)

def main():
   
    if constants.LIVE:
        process_live_data()
    else:
        process_recorded_data()


if __name__ == "__main__":
    # execute only if run as a script
    main()