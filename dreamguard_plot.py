# Calculate monitor data


if __name__ == '__main__':
    print(f">>> DREAMGUARD STARTUP\n")
    print(f"[ERROR] Start program with '_main.py'")
    exit()


# import modules
import traceback
import matplotlib.pyplot as plt
import numpy as np


# PLOT
def plot(monitor_reltime, resprate, heartrate, satrate,
         resprate_lim, heartrate_lim, satrate_lim, sensor_reltime,
         accx, accy, accz, gyrox, gyroy, gyroz):
    """define plots, graphs, legends
    show all monitor graphs in plot
    show accelerometer graphs when selected with mouse click
    show parameters of resprate, heartrate, satrate
    and time (since start of recording), when mouse moves over plot of monitor data
    """
    # FUNC SNAP CURSOR
    class SnaptoCursor(object):
        def __init__(self, ax, x, y):
            self.ax = ax
            self.ly = ax.axvline(color='k', alpha=0.2)  # the vert line
            self.marker, = ax.plot([0], [0], marker="o", color="crimson", zorder=3)
            self.x = x
            self.y = y
            self.txt = ax.text(0.7, 0.9, '')

        def mouse_move(self, event):
            """for mouse move set info to be shown"""
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
            self.marker.set_data([x], [y])
            self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
            self.txt.set_position((x, y))
            self.ax.figure.canvas.draw_idle()

    # Select accelerometer / gyro legend to hide / unhide graphs
    def on_pick(event):
        """show graphs of accelerometer when mouse pick"""
        legend = event.artist
        is_visible = legend.get_visible()
        graphs[legend].set_visible(not is_visible)
        legend.set_visible(not is_visible)
        fig.canvas.draw()

    # Update text for millis to h,m,s,ms
    def on_move(event):
        """calculate time since start of recording data
        show timestamp when mouse moves
        """
        global text

        # first time pointing in plot event artist "time" is not set,
        #   thus can not be removed
        # without remove() a new artist is created every time
        #   and overlap each other
        try:
            text.remove()
        except:
            pass

        # calc millis to timestamp and store artist in global variable
        #   to be able to remove/update it later
        if event.inaxes:
            millis = int(event.xdata)
            seconds = int( millis / 1000) % 60
            minutes = int(millis / (1000 * 60)) % 60
            hours = int(millis / (1000 * 60 * 60)) % 24
            text = ax1.text(0.5, -0.1, f"Timestamp: {hours}:{minutes}:{seconds}", transform=ax1.transAxes)

    try:
        # DEFINE PLOT PROPERTIES
        fig, (ax1, ax2) = plt.subplots(2, sharex=True)
        ax1.ticklabel_format(useOffset=False, style='plain')
        ax1.grid(True)
        ax2.grid(True)
        # ax1.set_xlabel('Time in ms')
        ax1.set_ylabel('Scale')
        ax2.set_ylabel('g-force OR deg-per-sec')
        ax2.set_xlabel('Time in ms')

        # DEFINE GRAPH PROPERTIES
        ax1.plot(monitor_reltime, resprate, color='limegreen', label='resprate')
        ax1.plot(monitor_reltime, resprate_lim, color='green')
        ax1.plot(monitor_reltime, heartrate, color='darkorange', label='heartrate')
        ax1.plot(monitor_reltime, heartrate_lim, color='red')
        ax1.plot(monitor_reltime, satrate, color='dodgerblue', label='satrate')
        ax1.plot(monitor_reltime, satrate_lim, color='blue')

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

        # Default hide all ax2 graphs
        for x in arraylegend:
            graphs[x].set_visible(False)
            x.set_visible(False)

        # Connect events
        # https://matplotlib.org/stable/gallery/event_handling/coords_demo.html
        # https://matplotlib.org/stable/gallery/text_labels_and_annotations/text_fontdict.html
        # https://matplotlib.org/stable/tutorials/text/text_props.html
        cursor = SnaptoCursor(ax1, monitor_reltime, resprate)
        cursor1 = SnaptoCursor(ax1, monitor_reltime, heartrate)
        cursor2 = SnaptoCursor(ax1, monitor_reltime, satrate)
        plt.connect('motion_notify_event', cursor.mouse_move)  
        plt.connect('motion_notify_event', cursor1.mouse_move)
        plt.connect('motion_notify_event', cursor2.mouse_move)
        plt.connect('motion_notify_event', on_move)
        plt.connect('pick_event', on_pick)

        # DRAW PLOT
        print(f'[INFO] Drawing plot.')
        plt.show()

    except:
        print(f"[ERROR] {traceback.format_exc()}")
        raise
