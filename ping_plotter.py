import matplotlib.pyplot as plt
import subprocess as sp
import sys
import time as clock

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


timeout_val = 1000 if sys.platform == "darwin" else 1

# 1 ping
# 1 sec timeout
ping_cmd = [ "ping", "-c", "1", "-W", str(timeout_val), ping_target ]

# Plot asthetics
plot_length = 60
plot_ping_fmt = "k-*"
plot_mean_fmt = "r:"
plot_jitter_fmt = "c.-"
plot_dropped_fmt = "b--."
plot_ping_label = "RTT Ping"
plot_mean_label = "RTT Ping Moving Average"
plot_jitter_label = "Jitter Moving Average"
plot_dropped_label = "Dropped Packets"
plot_title = "Ping Statistics to " + ping_target + " Plotted Over 60 Seconds"
plot_xlabel = "Time (s)"
plot_ylabel = "RTT Ping (ms)"

# X and Y axis data
iterations = []
ping_times = []

# Moving average
means = []

# Jitter moving average
jitter = []

# Dropped packet count
dropped = []

for i in range(0, plot_length):
    # Take start timestamp to keep the plot interval on
    # track
    start_ts = clock.time();

    # Add this round to the data set
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
        prev_jitter = get_last(jitter)
        prev_dropped = get_last(dropped)

        ping_times.append(prev_ping)
        means.append(prev_mean)
        jitter.append(prev_jitter)
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
    n = len(ping_times)
    prev_ping = get_last(ping_times)
    ping_times.append(time)

    # Compute mean
    prev_mean = get_last(means)
    new_mean = (prev_mean * n + time) / (n + 1)
    means.append(new_mean)

    # Compute jitter
    prev_jitter = get_last(jitter)
    cur_jitter = 0 if i == 0 else abs(time - prev_ping)
    new_jitter = (prev_jitter * n + cur_jitter) / (n + 1)
    jitter.append(new_jitter)

    # Dropped packets
    prev_dropped = get_last(dropped)
    dropped.append(prev_dropped)

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
    plt.plot(iterations, jitter, plot_jitter_fmt, label = plot_jitter_label)
    plt.plot(iterations, dropped, plot_dropped_fmt, label = plot_dropped_label)
    plt.legend(loc = "upper right")
    plt.draw()

    stop_ts = clock.time()
    elapsed_time = stop_ts - start_ts;

    # Pause for enough time to last ~1 second for this round
    pause_time = max(1.0 - elapsed_time, 0.00001)
    plt.pause(pause_time)

# Print stats
print("")
print("--- Statistics ---")
print("ping count = " + str(plot_length))
print("dropped count = " + str(get_last(dropped)))
print("mean rtt = " + str(get_last(means)) + " ms")
print("mean jitter = " + str(get_last(jitter)) + " ms")

# Wait indefinitely for user to close the plot
plt.pause(sys.maxsize)

