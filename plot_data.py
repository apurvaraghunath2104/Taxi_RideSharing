import matplotlib.pyplot as plt


def plot_data(avg_dist_saved_from, avg_trips_saved_from, runtime_from, avg_dist_saved_to, avg_trips_saved_to,
              runtime_to):
    x = [5, 10]

    y = [avg_dist_saved_from[0], avg_dist_saved_from[1]]
    plt.plot(x, y, marker='o', label="From Laguardia")
    y = [avg_dist_saved_to[0], avg_dist_saved_to[1]]
    plt.plot(x, y, marker='o', color="red", label="To Laguardia")
    plt.xlabel("Pool Size", fontsize=13)
    plt.ylabel("Average distance saved (%)", fontsize=13)
    plt.ylim(0.2, 0.5)
    plt.legend(loc="upper left")

    plt.show()

    y = [avg_trips_saved_from[0], avg_trips_saved_from[1]]
    plt.plot(x, y, marker='o', label="From Laguardia")
    y = [avg_trips_saved_to[0], avg_trips_saved_to[1]]
    plt.plot(x, y, marker='o', color="red", label="To Laguardia")
    plt.xlabel("Pool Size", fontsize=13)
    plt.ylabel("Average number of trips saved(%)", fontsize=13)
    plt.ylim(0.2, 0.55)
    plt.legend(loc="upper right")
    plt.show()

    y = [runtime_from[0], runtime_from[1]]
    plt.plot(x, y, marker='o', label="From Laguardia")
    y = [runtime_to[0], runtime_to[1]]
    plt.plot(x, y, marker='o', color="red", label="To Laguardia")
    plt.xlabel("Pool Size", fontsize=13)
    plt.ylabel("Runtime", fontsize=13)
    plt.legend(loc="upper left")
    plt.show()