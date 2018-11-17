
from auto_domain import Automobile, Edge
from config import config
import time

DEBUG = config["COMMON"]["DEBUG"]

# TODO -- if file already exists, rename the existing file and start a new one
# TODO -- some error handling would be nice!

data_filename = config["DEVICE"]["DEVICE_DATA_FILE"]
# assuming a data push model 
sampling_frequency = float(config["DEVICE"]["SAMPLING_FREQUENCY"])
sensors = config["DEVICE"]["SENSORS"]
print("Collecting and analyzing " + sensors +  " data.")
print("Sampling at the rate of every " + sampling_frequency +  "  second(s).")
if DEBUG:
    print("Echoing all data to: " + data_filename)


data_file = open(data_filename, "w")
# write the column headers
data_file.write(sensors)

device = Automobile(sensors)
edge = Edge(sensors)
i = 0
max =180000 # alternately forever -- till car stops!
while (i < max):
    i = i + 1
    time.sleep(sampling_frequency)
    line_text = device.read_sensors()
    print(line_text)
    data_file.write(line_text)
    edge.process_stream_data(line_text)
data_file.close()    

