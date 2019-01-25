from config import config

# common
DEBUG = config["COMMON"]["DEBUG"]

### Config related constants

DRIVER_NAME = config["DEVICE"]["DRIVER_NAME"]
DRIVER_ID = config["DEVICE"]["DRIVER_ID"]
VEHICLE_MODEL = config["DEVICE"]["VEHICLE_MODEL"]
VEHICLE_ID = config["DEVICE"]["VEHICLE_ID"]
HEAVY_VEHICLE = config["DEVICE"]["HEAVY_VEHICLE"]
SENSORS = config["DEVICE"]["SENSORS"]
DISTANCE_UNITS_LABEL= config["DEVICE"]["DISTANCE_UNITS_LABEL"]
GPS_SERIAL = config["DEVICE"]["GPS_SERIAL"]
GPS_BAUD_RATE = 4800
# fake gps co-ordinates till it becomes live 
DEFAULT_GPS = config["DEVICE"]["DEFAULT_GPS"]

LIVE = "True" == config["DEVICE"]["LIVE"]

SAMPLING_FREQUENCY = float(config["EDGE"]["SAMPLING_FREQUENCY"])
 
DATA_FILENAME = config["DEVICE"]["DEVICE_DATA_FILENAME"]

STREAM_TO_CLOUD = "True" == config["EDGE"]["STREAM_TO_CLOUD"]
RECORD = "True" == config["EDGE"]["RECORD"]

EVENTS_FILENAME = config["EDGE"]["EVENTS_FILENAME"]
EVENTS_FILENAME_BACKUP = config["EDGE"]["EVENTS_FILENAME_BACKUP"]
HISTORY = int(config["EDGE"]["HISTORY"])
MAX_READINGS = int(config["EDGE"]["MAX_READINGS"])

DRIVE_SAVE_FILENAME = config["EDGE"]["DRIVE_SAVE_FILENAME"]
DRIVE_SAVE_FILENAME_BACKUP = config["EDGE"]["DRIVE_SAVE_FILENAME_BACKUP"]

INSURANCE_ENABLED = "True" == config["EDGE"]["INSURANCE_ENABLED"]
MY_DRIVING_ENABLED = "True" == config["EDGE"]["MY_DRIVING_ENABLED"]
SMART_CITY_ENABLED = "True" == config["EDGE"]["SMART_CITY_ENABLED"]
REPORT_RETRY_SEC = int(config["EDGE"]["REPORT_RETRY_SEC"])
SAVE_INTERVAL_LOCAL = float(config["EDGE"]["SAVE_INTERVAL_LOCAL"])

## auto domain related constants

HARD_BREAK = "hard_break"
HARD_ACC = "hard_acc"
SPEEDING = "speeding"
NORMAL = "normal"
SLOW_DOWN = "slow_down"
MILES = "miles"
KMs = "kilometers"

INSURANCE_EVENTS = [HARD_BREAK, SPEEDING, HARD_ACC]


# Domain related
#http://tracknet.accountsupport.com/wp-content/uploads/Verizon/Hard-Brake-Hard-Acceleration.pdf
# Light and Medium Duty vehicles: 8.77 MPH/s | 14.11 KPH/s (0.40g)
# Heavy vehicles: 4.82 MPH/s | 7.76 KPH/s (0.22g)
# The maximum threshold for hard braking detection is 21.93 MPH/s | 35.29 KPH/s. Events above this threshold will still be
# captured by the Verizon Telematics 5500, however, regardless of the severity above this level the events will show 21.93
# | 35.29 as the severity.
# Hard Acceleration – How it works on 5500 Hardware
# Verizon Telematics defines a hard acceleration event as a sudden increase in speed greater than a minimum threshold
# as configured on the 5500 unit, causing excessive force on take-off or acceleration. The minimum thresholds for hard
# acceleration are:
# Light and Medium vehicles: 7.90 MPH/s | 12.71 KPH/s (0.36g)
# Heavy vehicles: 4.82 MPH/s | 7.76 KPH/s (0.22g) 
LIGHT_MEDIUM_HARD_BREAK = -8.77
HEAVY_HARD_BREAK = -4.82
LIGHT_MEDIUM_HARD_ACC = 7.9
HEAVY_HARD_ACC = 4.82

if HEAVY_VEHICLE :
    HARD_BREAK = HEAVY_HARD_BREAK
    HARD_ACC = HEAVY_HARD_ACC
else:
    HARD_BREAK = LIGHT_MEDIUM_HARD_BREAK
    HARD_ACC = LIGHT_MEDIUM_HARD_ACC

