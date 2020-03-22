# `ping_plotter`

I've been having consistent ping issues for a bit now for
some reason and I thought it might be useful to write a
little script to help me visualize/quantify those issues.

The purpose of this tool is simply to ping a single server
for however many times and then plot 3 metrics: the
round-trip time (RTT), the average RTT and finally the
numeber of ping packets lost.

# Implementation

This utilizes Python's `subprocess` module to run the
`ping` command several times. The results are then plotted
in real time using `matplotlib`.

Dropped packets repeat the previous time and maintain the
same mean.

# Usage

``` shell
git clone https://github.com/AgentTroll/ping_plotter.git
cd ping_plotter
python3 ping_plotter.py [ping_target]
```

Requires matplotlib (`pip3 install matplotlib`) and some
compatible GUI toolkit like python-tk (`apt-get install
python3-tk`) installed.

# Demo

![My RTT Ping to Github.com Over 30 Minutes](https://i.postimg.cc/tXdznDCk/11027188-36-Ping.png)

# Caveats

  * Unix (macOS/Linux) only - uses the `ping` command
  * Doesn't actually run in the plotted time, (e.g. 30
  min plotted will probably take around 40-45 minutes
  depending on who you are pinging)

# Credits

Built with [neovim](https://neovim.io/)

Uses [Matplotlib](https://matplotlib.org/)

