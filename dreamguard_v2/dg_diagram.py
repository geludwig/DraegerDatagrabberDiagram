# Calculate monitor data

# dependencies
import dg_global

# import modules
import matplotlib.pyplot as plt
import numpy as np


### PLOT ###
def calc_plot(monitor_reltime_norm, resprate_norm, heartrate_norm, satrate_norm, resprate_lim, heartrate_lim, satrate_lim, sensor_reltime, accx, accy, accz, gyrox, gyroy, gyroz):
    # FUNC SNAP CURSOR
    class SnaptoCursor(object):
        def __init__(self, ax, x, y):
            self.ax = ax
            self.ly = ax.axvline(color='k', alpha=0.2)  # the vert line
            self.marker, = ax.plot([0],[0], marker="o", color="crimson", zorder=3) 
            self.x = x
            self.y = y
            self.txt = ax.text(0.7, 0.9, '')

        def mouse_move(self, event):
            if not event.inaxes: return
            x, y = event.xdata, event.ydata
            indx = np.searchsorted(self.x, [x])[0]
            try:
                x = self.x[indx]
                y = self.y[indx]
            except:
                x = self.x[0]
                y = self.y[0]
            self.ly.set_xdata(x)
            self.marker.set_data([x],[y])
            self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
            self.txt.set_position((x,y))
            self.ax.figure.canvas.draw_idle()

    # FUNC SELECT GRAPH
    def on_pick(event):
        legend = event.artist
        isVisible = legend.get_visible()
        graphs[legend].set_visible(not isVisible)
        legend.set_visible(not isVisible)
        fig.canvas.draw()

    # DEFINE PLOT PROPERTIES
    fig, (ax1, ax2)  = plt.subplots(2, sharex=True)
    ax1.ticklabel_format(useOffset=False, style='plain')
    ax1.grid(True)
    ax2.grid(True)
    ax2.set_xlabel('Time in ms')
    ax1.set_ylabel('Scale1')
    ax2.set_ylabel('gravitational force OR degrees per sec')

    # DEFINE GRAPH PROPERTIES
    ax1.plot(monitor_reltime_norm, resprate_norm, color='limegreen', label='resprate')
    ax1.plot(monitor_reltime_norm, resprate_lim, color='green')
    ax1.plot(monitor_reltime_norm, heartrate_norm, color='darkorange', label='heartrate')
    ax1.plot(monitor_reltime_norm, heartrate_lim, color='red')
    ax1.plot(monitor_reltime_norm, satrate_norm, color='dodgerblue', label='satrate')
    ax1.plot(monitor_reltime_norm, satrate_lim, color='blue')

    axplt, = ax2.plot(sensor_reltime, accx, color='red', label='acc x', linewidth=0.6)
    ayplt, = ax2.plot(sensor_reltime, accy, color='green', label='acc y', linewidth=0.6)
    azplt, = ax2.plot(sensor_reltime, accz, color='blue', label='acc z', linewidth=0.6)
    gxplt, = ax2.plot(sensor_reltime, gyrox, color='red', label='gyro x', linewidth=0.6)
    gyplt, = ax2.plot(sensor_reltime, gyroy, color='green', label='gyro y', linewidth=0.6)
    gzplt, = ax2.plot(sensor_reltime, gyroz, color='blue', label='gyro z', linewidth=0.6)

    # DEFINE LEGENDS
    ax1.legend(loc='upper right')
    legend2 = ax2.legend(loc='upper right')
    axplt_legend2, ayplt_legend2, azplt_legend2, gxplt_legend2, gyplt_legend2, gzplt_legend2 = legend2.get_lines()

    # DEFINE PICKER
    arraylegend = [axplt_legend2, ayplt_legend2, azplt_legend2, gxplt_legend2, gyplt_legend2, gzplt_legend2]
    for x in arraylegend:
        x.set_picker(True)
        x.set_pickradius(10)

    # DEFINE GRAPHS
    graphs = {}
    graphs[axplt_legend2] = axplt
    graphs[ayplt_legend2] = ayplt
    graphs[azplt_legend2] = azplt
    graphs[gxplt_legend2] = gxplt
    graphs[gyplt_legend2] = gyplt
    graphs[gzplt_legend2] = gzplt

    # DEFAULT HIDE ALL AX2 GRAPHS
    for x in arraylegend:
        graphs[x].set_visible(False)
        x.set_visible(False)

    # CONNECT PLOT
    cursor = SnaptoCursor(ax1, monitor_reltime_norm, resprate_norm)
    cursor1 = SnaptoCursor(ax1, monitor_reltime_norm, heartrate_norm)
    cursor2 = SnaptoCursor(ax1, monitor_reltime_norm, satrate_norm)
    plt.connect('motion_notify_event', cursor.mouse_move)  
    plt.connect('motion_notify_event', cursor1.mouse_move)
    plt.connect('motion_notify_event', cursor2.mouse_move)
    plt.connect('pick_event', on_pick)

    # DRAW PLOT
    print('[INFO] Drawing plot.')
    plt.show() 