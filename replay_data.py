# supporting opportunistic data transmission
# should we have constant connectivity, it could have been a streaming application
# replay the data saved in a file and process as if in streaming mode!

from pathlib import Path
car_data = Path(DEVICE_DATA_FILE)
# TODO -- handle exceptions/error conditions
if car_data.is_file():
    data_file = open(config.CAR_DATA_FILE, "r")
    # first line contains table headers, indicates contents
    table_headers = data_file.readline()
    # global common variable
    CAR_DATA_PARSER = OBD_parser(table_headers)
    if DEBUG: 
        print(table_headers)

    for line in data_file:
        data_point = data_file.readline()
        if DEBUG:
            print(data_point)
        stream_data(obd_parser.process_data(line))
else:
    print("No car data to process! Bye!")