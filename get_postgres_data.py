from init_db import curr


def get_distance(lon1, lat1, lon2, lat2):
    curr.execute("select ST_DistanceSphere(ST_MakePoint(" + str(lon1) + "," + str(lat1) + "), ST_MakePoint(" + str(lon2) +
                 "," + str(lat2) + "))")
    distance = curr.fetchall()
    return (float(distance[0][0]) + 3000) / 1600


def get_nearest_point(lon, lat):
    # Get the nearest discretized point (this will be the user destination going forward)

    curr.execute("select lon, lat, ST_DistanceSphere(ST_MakePoint(lon, lat), ST_MakePoint(" + str(lon) + "," + str(lat) + ")) as dist " +
                 "from disc_manhattan_points where ST_DWithin(ST_SetSRID(ST_MakePoint(lon, lat), 4326), ST_SetSRID(ST_MakePoint(" + str(lon) + "," + str(lat) + "), 4326), 3000)" +
                 "order by dist limit 1")

    point = curr.fetchone()
    approximated_lon = point[0]
    approximated_lat = point[1]
    dist = point[2]
    return [approximated_lon, approximated_lat, dist]


def get_dropoffs(lon, lat):
    # For the approximated point get the dropoff points from the dropoffs table
    curr.execute("select drops from dropoffs_10 where lon = {0} and lat = {1}".format(lon, lat))
    result = curr.fetchall()
    if len(result) > 0:
        return result[0][0]
    else:
        return []