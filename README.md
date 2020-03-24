# `ping_plotter`

I've been having consistent ping issues for a bit now for
some reason and I thought it might be useful to write a
little script to help me visualize/quantify those issues.

The purpose of this tool is simply to ping a single server
for however many times and then plot 4 metrics: the
round-trip time (RTT), the average RTT, the average jitter
and finally the number of ping packets lost.

# Implementation

This utilizes Python's `subprocess` module to run the
`ping` command each second over a period of time. The
results are then plotted in real time using `matplotlib`.

Dropped packets repeat the previous time and maintain the
same mean.

# Usage

``` shell
git clone https://github.com/AgentTroll/ping_plotter.git
cd ping_plotter
python3 ping_plotter.py [ping_target]
```

Requires Python 3, matplotlib (`pip3 install -U
matplotlib`) and some compatible GUI toolkit like python-tk
(`apt-get install python3-tk`) installed.

# Demo

![Ping Statistics to github.com Plotted Over 60 Seconds](https://i.postimg.cc/wx2bdSR3/Ping.png)

```
--- Statistics ---
ping count = 60
dropped count = 4
mean rtt = 151.11627659281308 ms
mean jitter = 112.14193276703041 ms
```

# Caveats

  * Unix (macOS/Linux) only - uses the `ping` command
  * Makes a best-effort attempt to run in `plot_length`
  seconds, but this is not guaranteed depending how
  accurate the pause timer is and how long it takes for the
  plot to render on each round

# Credits

Built with [neovim](https://neovim.io/)

Uses [Matplotlib](https://matplotlib.org/)

