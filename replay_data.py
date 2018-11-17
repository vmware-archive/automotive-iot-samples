# supporting opportunistic data transmission
# should we have constant connectivity, it could have been a streaming application
# replay the data saved in a file and process as if in streaming mode!

from pathlib import Path
from config import config
# plugin pattern for generic functions
from auto_domain import Edge


DEBUG = config["COMMON"]["DEBUG"]
data_filename = config["DEVICE"]["DEVICE_DATA_FILE"]

# TODO -- handle exceptions/error conditions
if Path(data_filename).is_file():
    data_file = open(data_filename, "r", encoding='utf-8-sig')
    # first line contains table headers, indicates contents
    sensors_str = data_file.readline()
    if DEBUG:
        print("Sensor_str = " + sensors_str)
    if (sensors_str != "") :
        edge = Edge(sensors_str)
        for line in data_file:
            data_point = data_file.readline()
            if DEBUG:
                print(data_point)
            edge.process_stream_data(line)
    else:
        print("Data recording in incorrect format!") 
else:
    print("No car data to process! Bye!")