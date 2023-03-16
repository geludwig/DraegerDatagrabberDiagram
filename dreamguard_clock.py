'''Align reltimes of monitor and sensor data.'''


if __name__ == '__main__':
    print(f">>> DREAMGUARD STARTUP\n")
    print(f"[ERROR] Start program with '_main.py'")
    exit()


import traceback
import dreamguard_global


class Clock:
    '''Relative time of monitor and sensor data is aligned
    via their timestamps.
    '''

    def __init__(self, monitor_timestamp, monitor_reltime, resprate, heartrate,
                 satrate, resprate_lim, heartrate_lim, satrate_lim,
                 sensor_timestamp, sensor_reltime,
                 accx, accy, accz, gyrox, gyroy, gyroz):
        hertz = dreamguard_global.HERTZ
        maxtime = 60
        imonitor = 0
        isensor = 0

        try:
            if monitor_timestamp[0] < sensor_timestamp[0]:
                # monitor first, then sensor (monitor smaller)
                # if monitor was started before sensor
                # monitor data every 1 second, sensor every <hertz> millisecond
                # first step to check monitor array
                # which element is still smaller than sensor array
                # and delete all elements before from monitor array
                # second step to check sensor array
                # which element is still smaller than monitor array
                # and delete all elements before from sensor array
                # reason for second step is finer resolution from sensor
                # worst case after first step there can be a delta of 1 sec
                while (imonitor <= maxtime) and (monitor_timestamp[imonitor] < sensor_timestamp[0]):
                    imonitor = imonitor+1
                if imonitor > 0:
                    monitor_timestamp = monitor_timestamp[imonitor:] # from front
                if sensor_timestamp[0] < monitor_timestamp[0]:
                    while (isensor  <= hertz) and (sensor_timestamp[isensor ] < monitor_timestamp[0]):
                        isensor  += 1
                    if isensor > 0:
                        sensor_timestamp = sensor_timestamp[isensor:] # from front

            if sensor_timestamp[0] < monitor_timestamp[0]: # sensor first, then monitor (sensor smaller)
                while sensor_timestamp[isensor] < monitor_timestamp[0]:
                    isensor += 1
                if isensor > 0:
                    sensor_timestamp = sensor_timestamp[(isensor-1):] # from front
        except:
            print(f"[ERROR] {traceback.format_exc()}")
            raise
        
        try:
            monitor_reltime = monitor_reltime[imonitor:]
            sub = monitor_reltime[0]
            self.monitor_reltime = [x - sub for x in monitor_reltime]
            self.resprate = resprate[imonitor:]
            self.heartrate = heartrate[imonitor:]
            self.satrate = satrate[imonitor:]
            self.resprate_lim = resprate_lim[imonitor:]
            self.heartrate_lim = heartrate_lim[imonitor:]
            self.satrate_lim = satrate_lim[imonitor:]

            sensor_reltime = sensor_reltime[isensor:]
            sub = sensor_reltime[0]
            self.sensor_reltime = [x - sub for x in sensor_reltime]
            self.accx = accx[isensor:]
            self.accy = accy[isensor:]
            self.accz = accz[isensor:]
            self.gyrox = gyrox[isensor:]
            self.gyroy = gyroy[isensor:]
            self.gyroz = gyroz[isensor:]
        except:
            print(f"[ERROR] {traceback.format_exc()}")
            raise
        # print('[INFO] Aligned start times - monitor:', monitor_timestamp[0], ' sensor:', sensor_timestamp[0])
