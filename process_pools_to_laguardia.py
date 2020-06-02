from init_db import curr
import timeit
from get_postgres_data import get_dropoffs
from get_postgres_data import get_distance
from get_postgres_data import get_nearest_point
from max_match_dist_time_metrics import max_match
import json
import sys


def check_shareable_to_laguardia(src1, delay1, src2, delay2, src1_lag_dist, src2_lag_dist):

    src1_src2_dist = get_distance(src1[0], src1[1], src2[0], src2[1])
    src2_src1_dist = src1_src2_dist

    src1_lag_time = ((src1_lag_dist / 35) * 60) + 1.6 # Error of 1.6 min
    src2_lag_time = ((src2_lag_dist / 35) * 60) + 1.6
    src1_src2_time = ((src1_src2_dist / 35) * 60) + 1.6
    src2_src1_time = src1_src2_time

    if (src1_src2_dist + src2_lag_dist) < (src1_lag_dist + src2_lag_dist) and \
            (src1_src2_time + src2_lag_time) <= (src1_lag_time + delay1):
        return (src1_lag_dist + src2_lag_dist) - (src1_src2_dist + src2_lag_dist)

    elif (src2_src1_dist + src1_lag_dist) < (src1_lag_dist + src2_lag_dist) and \
            (src2_src1_time + src1_lag_time) <= (src2_lag_time + delay2):
        return (src1_lag_dist + src2_lag_dist) - (src2_src1_dist + src1_lag_dist)
    return -1


def main_to(pool, pno):
    pool_info = {}

    individual_trip_dist = {}
    start_time = timeit.default_timer()
    distance_error = 0
    dist = {}
    pool_info[pno] = {}
    total_num_trips = len(pool[pno]["destination"])
    total_dist = sum(pool[pno]["distance"])

    pool_info[pno]["total_num_trips"] = total_num_trips
    pool_info[pno]["total_dist"] = total_dist

    shareable_trips = []

    for i in range(len(pool[pno]["pickup"])):

        min_non_share_dist = sys.maxsize
        if i not in individual_trip_dist.keys():
            individual_trip_dist[i] = pool[pno]["distance"][i]

        num_shareable = 0
        dist[i+1] = {}
        trip_1 = pool[pno]["pickup"][i]
        src1 = get_nearest_point(trip_1[0], trip_1[1])
        distance_error += src1[2]

        curr.execute("select time from lag_pt_dist_time where lon2 = " + str(src1[0]) + " and lat2 = " + str(src1[1]))

        result = curr.fetchall()
        if len(result) > 0:
            delay1 = 0.2 * float(result[0][0] / 60)
        else:
            travel_time = ((individual_trip_dist[i] / 35) * 60) + 1.6
            delay1 = 0.2 * float(travel_time)

        for j in range(i+1, len(pool[pno]["pickup"])):
            if j not in individual_trip_dist.keys():
                individual_trip_dist[j] = pool[pno]["distance"][j]

            trip_2 = pool[pno]["pickup"][j]
            src2 = get_nearest_point(trip_2[0], trip_2[1])[:-1]
            new_distance = get_distance(src1[0], src1[1], src2[0], src2[1])
            
            # To remove optimization and process all combination of trips, comment the following 2 lines
            if new_distance > min_non_share_dist:
                continue

            curr.execute("select time from lag_pt_dist_time where lon2 = " + str(src2[0]) + " and lat2 = " + str(src2[1]))
            result = curr.fetchall()
            if len(result) > 0:
                delay2 = 0.2 * float(result[0][0] / 60)
            else:
                travel_time = ((individual_trip_dist[i] / 35) * 60) + 1.6
                delay2 = 0.2 * float(travel_time)

            dist_saved = check_shareable_to_laguardia(src1, delay1, src2, delay2, individual_trip_dist[i], individual_trip_dist[j])

            if dist_saved != -1:
                num_shareable += 1
                shareable_trips.append((i+1, j+1, round(dist_saved)))
                dist[i+1][j+1] = dist_saved

                if (j+1) not in dist.keys():
                    dist[j+1] = {}
                dist[j+1][i+1] = dist_saved
            else:
                # Update min_non_share_dist
                min_non_share_dist = new_distance

        print("Trip {0} done. {1} trips shareable with this trip.".format(i+1, num_shareable))

    distance_error /= pool_info[pno]["total_num_trips"]
    pool_info[pno]["average_distance_error"] = distance_error
    pool_info = max_match(shareable_trips, pno, pool_info, dist, timeit.default_timer() - start_time)

    print("Pool {0} done.\n".format(pno))
    return pool_info
