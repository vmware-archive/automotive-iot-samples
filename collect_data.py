import obd
# import auto_domain_knowledge
import serial
import sys
import time
from config import config


SPEED_CMD = obd.commands.SPEED
RPM_CMD = obd.commands.RPM
FUEL_LEVEL_CMD = obd.commands.FUEL_LEVEL
RELATIVE_ACCEL_POS_CMD = obd.commands.RELATIVE_ACCEL_POS
ABSOLUTE_LOAD_CMD = obd.commands.ABSOLUTE_LOAD
ENGINE_LOAD_CMD = obd.commands.ENGINE_LOAD
RELATIVE_THROTTLE_POS_CMD = obd.commands.RELATIVE_THROTTLE_POS
THROTTLE_POS_B_CMD = obd.commands.THROTTLE_POS_B
THROTTLE_POS_C_CMD = obd.commands.THROTTLE_POS_C

cmd_list = [
        SPEED_CMD,
        RPM_CMD,
        FUEL_LEVEL_CMD,
        #RELATIVE_ACCEL_POS_CMD,
        ABSOLUTE_LOAD_CMD,
        ENGINE_LOAD_CMD,
        RELATIVE_THROTTLE_POS_CMD,
        THROTTLE_POS_B_CMD,
        #THROTTLE_POS_C_CMD
        ]

connection = obd.OBD()

max =180000 # alternately forever -- till car stops!
i = 0

# TODO -- if file already exists, rename the existing file and start a new one
# TODO -- some error handling would be nice!

data_file = open(DEVICE_DATA_FILE, "w")
# write the column headers
headers = "SPEED, RPM, FUEL_LEVEL, ABSOLUTE_LOAD, ENGINE_LOAD, RELATIVE_THROTTLE_POS, THROTTLE_POS_B"
print(headers)
data_file.write(headers)
auto_domain_knowledge.OBD_parser(headers)

while (i < max):
    i = i + 1
    time.sleep(SAMPLING_FREQUENCY)
    # going through list of commands
    line_text = str(time.time()) + ", " #new row with time
    for cmd in cmd_list:
        # appending results to row
        try:
            # TODO add GPS co-ordinates too .. else we shall need to track a separate file and
            # match up data based on time stamp
            line_text += str(connection.query(cmd).value.magnitude) + ", "
        except:
            line_text +=  "Error, "
            print("Unexpected error:", sys.exc_info()[0])
    print(line_text)
    data_file.write(line_text)
    auto_domain_knowledge.stream_data(line_text)

data_file.close()    

