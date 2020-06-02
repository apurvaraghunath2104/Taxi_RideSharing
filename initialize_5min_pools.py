from datetime import datetime
from datetime import timedelta
from process_pools_from_laguardia import main_from
from process_pools_to_laguardia import main_to
import json


def get_date(date_string):
    try:
        date = datetime.strptime(date_string, '%m/%d/%Y')
    except ValueError:
        date = datetime.strptime(date_string, '%Y-%m-%d')
    return date


def get_time(time_string):
    try:
        time = datetime.strptime(time_string, '%H:%M')
    except ValueError:
        time = datetime.strptime(time_string, '%H:%M:%S')
    return time


def initialize_pool_5_min(trips, direction):
    pools = {}
    pool_5_ongoing = False
    pool_5_index = 0
    pickup_coord_5 = []
    destination_coord_5 = []
    distance_5 = []
    i = 0
    start_date = None

    while i < len(trips["vendorid"]):

        if start_date is None:
            start_date = get_date(trips["tpep_pickup_datetime"][i].split()[0])
        else:
            current_date = get_date(trips["tpep_pickup_datetime"][i].split()[0])
            if current_date > start_date:
                start_date = get_date(trips["tpep_pickup_datetime"][i].split()[0])
                pool_5_ongoing = False

        if not pool_5_ongoing:
            pool_5_ongoing = True
            pool_5_index += 1
            pools[pool_5_index] = {}
            pickup_coord_5 = [(trips["pickup_longitude"][i], trips["pickup_latitude"][i])]
            destination_coord_5 = [(trips["dropoff_longitude"][i], trips["dropoff_latitude"][i])]
            distance_5 = [trips["trip_distance"][i]]
            start_5_min = trips["tpep_pickup_datetime"][i].split()[1]

        else:
            current_time = trips["tpep_pickup_datetime"][i].split()[1]
            if get_time(current_time) > (get_time(start_5_min) + timedelta(
                    minutes=5)):
                print("Pool {0} obtained".format(pool_5_index))

                pool_5_ongoing = False
                pools[pool_5_index]["pickup"] = pickup_coord_5
                pools[pool_5_index]["destination"] = destination_coord_5
                pools[pool_5_index]["distance"] = distance_5

                # Call main_from or main_to from here
                if direction == "to":

                    # If you are just starting to process a month from the 1st day, then change the condition to be ' >= 0 '
                    if pool_5_index >= 0: # If program stopped for some reason, change this number to be the pool number after the last pool processed
                        pool_info = main_to(pools, pool_5_index)
                        global_pool_info[pool_5_index] = pool_info[pool_5_index]

                        # Create the month's folder inside the folder 5min_pools_info (or whatever folder name you are using)
                        # and save the file inside that folder
                        with open("D:\\UIC\\Database Management Systems\\Taxi Ridesharing\\5min_pools_info\\January\\pool_5min_to_laguardia.json", "w") as fp:
                            json.dump(global_pool_info, fp)
                else:

                    # If you are just starting to process a month from the 1st day then change the condition to be ' >= 0 '
                    if pool_5_index >= 0: # If program stopped for some reason, change this number to be the pool number after the last pool processed
                        pool_info = main_from(pools, pool_5_index)
                        global_pool_info[pool_5_index] = pool_info[pool_5_index]

                        # Create the month's folder inside the folder 5min_pools_info (or whatever folder name you are using)
                        # and save the file inside that folder
                        with open("D:\\UIC\\Database Management Systems\\Taxi Ridesharing\\5min_pools_info\\January\\pool_5min_from_laguardia.json", "w") as fp:
                            json.dump(global_pool_info, fp)
                continue

            else:
                pickup_coord_5.append((trips["pickup_longitude"][i], trips["pickup_latitude"][i]))
                destination_coord_5.append((trips["dropoff_longitude"][i], trips["dropoff_latitude"][i]))
                distance_5.append(trips["trip_distance"][i])
        i += 1
        if pool_5_ongoing:
            pools[pool_5_index]["pickup"] = pickup_coord_5
            pools[pool_5_index]["destination"] = destination_coord_5
            pools[pool_5_index]["distance"] = distance_5


global_pool_info = {}
