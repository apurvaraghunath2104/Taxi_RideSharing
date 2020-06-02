import json


def find_num_trips(pool):
    total_num_trips = []
    num_trips_saved = []
    avg_trips_saved = []

    for pno in pool.keys():
        avg_trips_saved.append(pool[pno]["num_trips_saved"] / pool[pno]["total_num_trips"])
        total_num_trips.append(pool[pno]["total_num_trips"])
        num_trips_saved.append(pool[pno]["num_trips_saved"])

    avg_num_trips = sum(total_num_trips) / len(total_num_trips)
    avg_num_trips_saved = sum(num_trips_saved) / len(num_trips_saved)

    return avg_num_trips_saved / avg_num_trips


def find_avg_distance_saved(pool):
    total_distance = []
    distance_saved = []
    avg_distance_saved = []

    for pno in pool.keys():

        total_distance.append(pool[pno]["total_dist"])
        distance_saved.append(pool[pno]["dist_saved"])
        if pool[pno]["total_dist"] != 0.0:
            avg_distance_saved.append(pool[pno]["dist_saved"] / pool[pno]["total_dist"])

    avg_total_distance = sum(total_distance) / len(total_distance)
    avg_dist_saved = sum(distance_saved) / len(distance_saved)

    return avg_dist_saved / avg_total_distance


def find_runtime(pool):
    runtime = []

    for pno in pool.keys():
        runtime.append(pool[pno]["runtime"])

    return sum(runtime) / len(runtime)


def find_trips_per_pool(pool):
    no_of_pools = []
    for pno in pool.keys():
        no_of_pools.append(pool[pno]["total_num_trips"])

    return round(sum(no_of_pools) / len(no_of_pools))


def find_total_trips(pool):
    trips = 0
    for pno in pool.keys():
        trips += pool[pno]["total_num_trips"]
    return trips


def find_distance_error(pool):
    error = 0
    for pno in pool.keys():
        error += pool[pno]["average_distance_error"]
    return error / len(pool.keys())
