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
    if drive.save_time():
        auto_domain.log_distance(drive.total_distance_unit)
    event_type = auto_domain.get_event_type(drive, data_dict)
    if not (event_type == constants.NORMAL):
        data_dict["EVENT_TYPE"] = event_type  # data_dict enhanced with event_type 
        auto_domain.log_auto_event(event_type, data_dict)  
        drive.update_events(data_dict)
        if constants.STREAM:
            report_event(data_dict, drive.autoID)
    

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
                    drive = Drive(autoID,constants.SAMPLING_FREQUENCY, constants.HISTORY)
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


def process_live_data():
    autoID =  AutoID(constants.DRIVER_NAME, constants.DRIVER_ID, constants.VEHICLE_MODEL, constants.VEHICLE_ID)
    automobile = Automobile(autoID, constants.SENSORS)
    drive = Drive(autoID, constants.SAMPLING_FREQUENCY, constants.HISTORY)
    with open(constants.DATA_FILENAME, 'w') as file:
        for i in range(constants.MAX_READINGS):
        # while (True):
            data_dict = automobile.read_sensors()
            if data_dict:
                # record the data to revisit ..
                file.write(automobile.to_compact_str(data_dict)) 
                process_stream_data(drive, data_dict) 
            time.sleep(constants.SAMPLING_FREQUENCY)

def main():
    # sensors_str = "TIME, SPEED, RPM, FUEL_LEVEL, ABSOLUTE_LOAD, ENGINE_LOAD, RELATIVE_THROTTLE_POS, THROTTLE_POS_B" 
    # dp = DataParser(sensors_str)
    # dp.parse("1537304004,39,2690,28.23529412,42.35294118,23.92156863,11.76470588,22.35294118, ")
   
    if constants.LIVE:
        process_live_data()
    else:
        process_recorded_data()


if __name__ == "__main__":
    # execute only if run as a script
    main()