import matplotlib.pyplot as plt
import subprocess as sp
import sys

# Get last element or 0 if the list is empty
def get_last(x):
    x_list = list(x)
    return 0 if not x_list else x_list[-1]

# Args check
if len(sys.argv) != 2:
    print("Ping target required")
    sys.exit(0)

ping_target = sys.argv[1]
print("ping_target = " + ping_target)

ping_cmd = [ "ping", "-c", "1", ping_target ]

# Plot asthetics
plot_length = 60
plot_ping_fmt = "k-*"
plot_mean_fmt = "r:"
plot_dropped_fmt = "b--."
plot_ping_label = "RTT Ping"
plot_mean_label = "RTT Ping Moving Average"
plot_dropped_label = "Dropped Packets"
plot_title = "My RTT Ping to " + ping_target + " Over 60 Seconds"
plot_xlabel = "Time (s)"
plot_ylabel = "RTT Ping (ms)"

# X and Y axis data
iterations = []
ping_times = []

# Moving average
means = []

# Dropped packet count
dropped = []

for i in range(0, plot_length):
    iterations.append(i)

    # Run the ping command
    run_result = sp.run(ping_cmd, stdout = sp.PIPE)

    # Process the ping output
    output_str = str(run_result.stdout)
    output_arr = output_str.split("\\n")
    comp = output_arr[1]

    # Dropped packet - no response string to parse
    if comp == "":
        print("Packet dropped")

        # Update data to reflect dropped packet
        # ST for ping and +1 dropped
        prev_ping = get_last(ping_times)
        prev_mean = get_last(means)
        prev_dropped = get_last(dropped)

        ping_times.append(prev_ping)
        means.append(prev_mean)
        dropped.append(prev_dropped + 1)
        continue

    # Print component string for debugging purposes
    print(comp)

    time_eq_idx = comp.rfind("=")
    time_space_idx = comp.rfind(" ")
    time_str = comp[time_eq_idx + 1:time_space_idx]

    # Select the time and convert to a number
    time = float(time_str)

    # Add to the axis data
    ping_times.append(time)

    # Compute mean
    n = len(means)
    prev_mean = get_last(means)
    new_mean = (prev_mean * n + time) / (n + 1)

    prev_dropped = get_last(dropped)
    dropped.append(prev_dropped)

    # Add mean to axis
    means.append(new_mean)

    # Plot asthetics
    plt.clf()
    plt.ion()
    plt.title(plot_title)
    plt.xlabel(plot_xlabel)
    plt.ylabel(plot_ylabel)
    plt.grid()

    # Plot the data
    plt.plot(iterations, ping_times, plot_ping_fmt, label = plot_ping_label)
    plt.plot(iterations, means, plot_mean_fmt, label = plot_mean_label)
    plt.plot(iterations, dropped, plot_dropped_fmt, label = plot_dropped_label)
    plt.legend(loc = "upper right")
    plt.draw()
    plt.pause(1)

# Print stats
print("")
print("--- Statistics ---")
print("ping count = " + str(plot_length))
print("dropped count = " + str(get_last(dropped)))
print("mean rtt = " + str(get_last(means)))

# Wait indefinitely for user to close the plot
plt.pause(sys.maxsize)

