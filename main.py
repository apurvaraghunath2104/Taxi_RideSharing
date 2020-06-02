import pandas as pd
import initialize_5min_pools
import initialize_10min_pools
from final_results import find_trips_per_pool
from final_results import find_runtime
from final_results import find_avg_distance_saved
from final_results import find_num_trips
from final_results import find_total_trips
from final_results import find_distance_error
from plot_data import plot_data
import json


# Set direction to either from / to.
direction = "from"

# Open the correct trips csv file
trips = pd.read_csv("../Yellow Tripdata 2016 (Till May)/trips_{}_laguardia_jan_2016.csv".format(direction))

# Call either initialize_5min_pools() or initialize_10min_pools() (it will fetch pools on the go and process them)

# initialize_5min_pools.initialize_pool_5_min(trips, direction)
initialize_10min_pools.initialize_pool_10_min(trips, direction)

# Open the appropriate pool info files below
# with open("D:\\UIC\\Database Management Systems\\Taxi Ridesharing\\5min_pools_info\\March\\pool_5min_from_laguardia_march.json") as fp:
#     pool_5min_from = json.load(fp)
#
# with open("D:\\UIC\\Database Management Systems\\Taxi Ridesharing\\5min_pools_info\\March\\pool_5min_to_laguardia.json") as fp:
#     pool_5min_to = json.load(fp)
#
# with open("D:\\UIC\\Database Management Systems\\Taxi Ridesharing\\10min_pools_info\\March\\pool_10min_from_laguardia_from_1.json") as fp:
#     pool_10min_from = json.load(fp)
#
# with open("D:\\UIC\\Database Management Systems\\Taxi Ridesharing\\10min_pools_info\\March\\pool_10min_to_laguardia_march.json") as fp:
#     pool_10min_to = json.load(fp)
#
#
# The functions below will compute the average distance saved, trips saved and the runtime recorded
#
# avg_dist_saved_from = [(find_avg_distance_saved(pool_5min_from)), find_avg_distance_saved(pool_10min_from_modified)]
# avg_trips_saved_from = [(find_num_trips(pool_5min_from)), find_num_trips(pool_10min_from_modified)]
# runtime_from = [find_runtime(pool_5min_from), find_runtime(pool_10min_from_modified)]
#
# avg_dist_saved_to = [(find_avg_distance_saved(pool_5min_to)), find_avg_distance_saved(pool_10min_to_modified)]
# avg_trips_saved_to = [(find_num_trips(pool_5min_to)), find_num_trips(pool_10min_to_modified)]
# runtime_to = [find_runtime(pool_5min_to), find_runtime(pool_10min_to_modified)]
# # print(find_distance_error(pool_10min_from))

# plot_data(avg_dist_saved_from, avg_trips_saved_from, runtime_from, avg_dist_saved_to, avg_trips_saved_to, runtime_to)
