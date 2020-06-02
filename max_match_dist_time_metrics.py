import maximum_weight_matching


def max_match(shareable_trips, pool_no, pool_info, dist, runtime):
    mates = maximum_weight_matching.max_weight_matching(shareable_trips)
    count = 0
    total_dist_shared = 0

    for i in range(1, len(mates)):
        if mates[i] == -1:
            count += 1
        else:
            mates[mates[i]] = -1
            total_dist_shared += dist[i][mates[i]]

    if count == 0:
        pool_info[pool_no]["num_trips_saved"] = 0
    else:
        pool_info[pool_no]["num_trips_saved"] = pool_info[pool_no]["total_num_trips"] - count

    pool_info[pool_no]["dist_saved"] = total_dist_shared
    pool_info[pool_no]["runtime"] = runtime

    return pool_info
