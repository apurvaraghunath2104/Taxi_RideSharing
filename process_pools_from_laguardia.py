from init_db import curr
import timeit
from get_postgres_data import get_distance
from get_postgres_data import get_nearest_point
from get_postgres_data import get_dropoffs
from max_match_dist_time_metrics import max_match
import json
import sys

def no_walks_shareable(dest1, delay1, dest2, delay2, src, src_dest1_dist, src_dest2_dist):

    dest1_dest2_dist = get_distance(dest1[0], dest1[1], dest2[0], dest2[1])
    dest2_dest1_dist = dest1_dest2_dist

    dest1_dest2_time = ((dest1_dest2_dist / 35) * 60) + 1.6
    dest2_dest1_time = dest1_dest2_time

    curr.execute("select time from lag_pt_dist_time where lon1 = " + str(src[0]) + " and lat1 = " + str(src[1]) + " and lon2 = "
                 + str(dest1[0]) + " and lat2 = " + str(dest1[1]))
    result = curr.fetchall()
    if len(result) > 0:
        src_dest1_time = float(result[0][0] / 60)
    else:
        src_dest1_time = ((src_dest1_dist / 35) * 60) + 1.6

    curr.execute("select time from lag_pt_dist_time where lon1 = " + str(src[0]) + " and lat1 = " + str(src[1]) + " and lon2 = "
                 + str(dest2[0]) + " and lat2 = " + str(dest2[1]))
    result = curr.fetchall()
    if len(result) > 0:
        src_dest2_time = float(result[0][0] / 60)
    else:
        src_dest2_time = ((src_dest2_dist / 35) * 60) + 1.6

    if (src_dest1_dist + dest1_dest2_dist) < (src_dest1_dist + src_dest2_dist) and \
    (src_dest1_time + dest1_dest2_time) <= (src_dest2_time + delay2):
        return (src_dest1_dist + src_dest2_dist) - (src_dest1_dist + dest1_dest2_dist)

    elif (src_dest2_dist + dest2_dest1_dist) < (src_dest1_dist + src_dest2_dist) and \
            (src_dest2_time + dest2_dest1_time) <= (src_dest1_time + delay1):
        return (src_dest1_dist + src_dest2_dist) - (src_dest2_dist + dest2_dest1_dist)

    else:
        return -1


def check_walk_shareable(src, dest1, delay1, drops1, dest2, delay2, drops2, src_dest1_dist, src_dest2_dist):
    curr.execute("select dist, time from lag_pt_dist_time where lon1 = " + str(src[0]) + " and lat1 = " + str(src[1]) +
                 " and lon2 = " + str(dest1[0]) + " and lat2 = " + str(dest1[1]))
    result = curr.fetchall()
    # src_dest1_dist = float(result[0])
    if len(result) > 0:
        src_dest1_time = float(result[0][1] / 60)
    else:
        src_dest1_time = ((src_dest1_dist / 35) * 60) + 1.6

    curr.execute("select dist, time from lag_pt_dist_time where lon1 = " + str(src[0]) + " and lat1 = " + str(src[1]) +
                 " and lon2 = " + str(dest2[0]) + " and lat2 = " + str(dest2[1]))
    result = curr.fetchall()
    # src_dest2_dist = float(result[0])
    if len(result) > 0:
        src_dest2_time = float(result[0][1] / 60)
    else:
        src_dest2_time = ((src_dest2_dist / 35) * 60) + 1.6

    for drop in drops1:
        # Drop rider1 first
        src_drop_dist = get_distance(src[0], src[1], drop[0], drop[1])
        src_drop_time = ((src_drop_dist / 35) * 60) + 1.6

        drop_dest2_dist = get_distance(drop[0], drop[1], dest2[0], dest2[1])
        drop_dest2_time = ((drop_dest2_dist / 35) * 60) + 1.6

        if (src_drop_dist + drop_dest2_dist) < (src_dest1_dist + src_dest2_dist) and \
        (src_drop_time + drop_dest2_time) <= (src_dest2_time + delay2):
            return (src_dest1_dist + src_dest2_dist) - (src_drop_dist + drop_dest2_dist)

    for drop in drops2:
        # Drop rider2 first
        src_drop_dist = get_distance(src[0], src[1], drop[0], drop[1])
        src_drop_time = ((src_drop_dist / 35) * 60) + 1.6 # Error of ~ 1.6 min

        drop_dest1_dist = get_distance(drop[0], drop[1], dest1[0], dest1[1])
        drop_dest1_time = ((src_drop_dist / 35) * 60) + 1.6

        if (src_drop_dist + drop_dest1_dist) < (src_dest1_dist + src_dest2_dist) and \
                (src_drop_time + drop_dest1_time) <= (src_dest1_time + delay1):
            return (src_dest1_dist + src_dest2_dist) - (src_drop_dist + drop_dest1_dist)

    return -1


def main_from(pool, pno):
    pool_info = {}

    start_time = timeit.default_timer()
    pool_info[pno] = {}
    dist = {}
    individual_trip_dist = {}
    total_num_trips = len(pool[pno]["destination"])
    total_dist = sum(pool[pno]["distance"])
    distance_error = 0
    pool_info[pno]["total_num_trips"] = total_num_trips
    pool_info[pno]["total_dist"] = total_dist

    shareable_trips = []

    # Go over each trip A
    for i in range(len(pool[pno]["destination"])):
        min_non_share_dist = sys.maxsize

        if i not in individual_trip_dist.keys():
            individual_trip_dist[i] = pool[pno]["distance"][i]

        num_shareable = 0
        print("Trip {0} started".format(i+1))
        dist[i+1] = {}
        trip_1 = pool[pno]["destination"][i]
        dest1 = get_nearest_point(trip_1[0], trip_1[1])
        distance_error += dest1[2]
        drops1 = get_dropoffs(dest1[0], dest1[1])

        curr.execute("select time from lag_pt_dist_time where lon2 = " + str(dest1[0]) + " and lat2 = " + str(dest1[1]))
        result = curr.fetchall()
        if len(result) > 0:
            delay1 = 0.2 * float(result[0][0] / 60) # 20% delay

        else: # No travel time is precomputed for this pair of points
            travel_time = ((individual_trip_dist[i] / 35) * 60) + 1.6
            delay1 = 0.2 * float(travel_time)

        for j in range(i+1, len(pool[pno]["destination"])): # Go over every other trip B


            if j not in individual_trip_dist.keys():
                individual_trip_dist[j] = pool[pno]["distance"][j]

            trip_2 = pool[pno]["destination"][j]
            dest2 = get_nearest_point(trip_2[0], trip_2[1])[:-1]
            new_distance = get_distance(dest1[0], dest1[1], dest2[0], dest2[1])
            
            # To remove optimization and process all combination of trips, comment the following 2 lines
            if new_distance > min_non_share_dist:
                continue

            drops2 = get_dropoffs(dest2[0], dest2[1])

            curr.execute(
                "select time from lag_pt_dist_time where lon2 = " + str(dest2[0]) + " and lat2 = " + str(dest2[1]))
            result = curr.fetchall()
            if len(result) > 0:
                delay2 = 0.2 * float(result[0][0] / 60)

            else: # No travel time precomputed for this pair of points
                travel_time = ((individual_trip_dist[i] / 35) * 60) + 1.6
                delay2 = 0.2 * float(travel_time)

            dist_saved = no_walks_shareable(dest1, delay1, dest2, delay2, [-73.874, 40.774],
                                            individual_trip_dist[i], individual_trip_dist[j])

            if dist_saved != -1:
                num_shareable += 1
                shareable_trips.append((i+1, j+1, round(dist_saved)))
                dist[i+1][j+1] = dist_saved
                if (j+1) not in dist.keys():
                    dist[j+1] = {}
                dist[j+1][i+1] = dist_saved

            else:
                dist_saved = check_walk_shareable([-73.874, 40.774], dest1, delay1, drops1, dest2, delay2, drops2,
                                                  individual_trip_dist[i], individual_trip_dist[j])
                if dist_saved != -1:
                    num_shareable += 1
                    shareable_trips.append((i+1, j+1, round(dist_saved)))
                    dist[i+1][j+1] = dist_saved
                    if (j+1) not in dist.keys():
                        dist[j+1] = {}
                    dist[j+1][i+1] = dist_saved

                else:
                    # Update min_non_share_distance
                    if new_distance < min_non_share_dist:
                        min_non_share_dist = new_distance

        print("Trip {0} done. {1} trips shareable with this trip.".format(i+1, num_shareable))

    distance_error /= pool_info[pno]["total_num_trips"]
    pool_info[pno]["average_distance_error"] = distance_error
    pool_info = max_match(shareable_trips, pno, pool_info, dist, timeit.default_timer() - start_time)

    print("Pool {0} done.".format(pno))
    return pool_info
