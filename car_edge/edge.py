from config import config
from auto import AutoID, Automobile, DataParser, Drive
import auto_domain 
import constants
from report import report_event
from pathlib import Path
import sys
import time
import datetime


def process_stream_data(drive, data_dict):
    print("enter process_stream_data")
    drive.data_buffer.add(data_dict)
    if "SPEED" in data_dict:
        # from OBD sensor
        drive.update_distance(data_dict["SPEED"])
    elif "speed" in data_dict:
        # from GPS
        drive.update_distance(data_dict["speed"])
    drive.inc_samples()
    if ((drive.begin_fuel_level < 0) and ("FUEL_LEVEL" in data_dict)):
        drive.begin_fuel_level = float(data_dict["FUEL_LEVEL"])

    if drive.analysis_time():
        drive_event = auto_domain.check_for_events_of_interest(drive.data_buffer)
        if not (drive_event == constants.NORMAL):
            data_dict["EVENT_TYPE"] = drive_event  # data_dict enhanced with event_type 
            auto_domain.log_auto_event(drive_event, data_dict)  
            drive.update_events(data_dict)
            if constants.STREAM_TO_CLOUD:
                report_event(data_dict, drive.autoID)
    # periodically persist distance traveled to local filesystem 
    if drive.save_time():
        auto_domain.save(drive)

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


def record_metrics_header(metric_list, output_file_name):
    """
    write header for each available sensor/metric
    """
    with open(output_file_name, 'w') as file:
        # writting each metric on the header
        file.write(",".join(metric_list)+"\n")


def record_sensor_readings(data_dict, metric_list, output_file_name):
    """
    Write data row to output file
    """
    sensor_vals = []
    # going though metric_list to keep order consistent
    for metric in metric_list:
        if metric in data_dict:
            sensor_vals.append(str(data_dict[metric]))
        else:
            # value not recorded properly
            sensor_vals.append("null")
    vals =  ",".join(sensor_vals)

    # write to file
    # TODO: keep file open for duration of the drive to avoid re-opening it at each iteration
    with open(output_file_name, 'a') as file:
        file.write(vals+"\n")


def process_live_data():

    autoID =  AutoID(constants.DRIVER_NAME, constants.DRIVER_ID, constants.VEHICLE_MODEL, constants.VEHICLE_ID)
    automobile = Automobile(autoID, constants.SENSORS)
    drive = Drive(autoID, constants.SAMPLING_FREQUENCY, constants.HISTORY, constants.SAVE_INTERVAL_LOCAL)


    # Printing headers to file (Depending on data points defined in config file)
    metric_list = None
    output_file_name = None
    if len(automobile.sensors_connections) > 0:
        if constants.RECORD:
            metric_list = automobile.get_tracked_metrics()

            now = datetime.datetime.now()
            output_file_name = "data/drive_" + now.strftime("%A_%d_%B_%Y_%I_%M%p") + ".csv"
            print("Writting data to :" + output_file_name)
            record_metrics_header(metric_list, output_file_name)

        while True:
            # reads the data from the various sensors
            data_dict = automobile.read_sensors()

            if data_dict:
                process_stream_data(drive, data_dict)
            
            # TODO: print data to file if recorded. Make sure all data is in and all
            if constants.RECORD and metric_list:
                record_sensor_readings(data_dict,metric_list, output_file_name)

            time.sleep(constants.SAMPLING_FREQUENCY)
    else:
        print("No sensor connected. Please make sure sensors are connected. \n Bye!")

def main():
    if constants.LIVE:
        process_live_data()
    else:
        process_recorded_data()


if __name__ == "__main__":
    # execute only if run as a script
    main()