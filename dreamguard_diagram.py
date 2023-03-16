'''Diagram class which does all necessary steps to create a diagram.'''


if __name__ == '__main__':
    print(f">>> DREAMGUARD STARTUP\n")
    print(f"[ERROR] Start program with '_main.py'")
    exit()


import dreamguard_import
import dreamguard_monitor
import dreamguard_sensor
import dreamguard_clock
import dreamguard_plot


class Diagram:
    """Creates new diagram class.
    Functions defined here are called as objects to return multiple values.
    Other Options to return multiple values: tuple, list, dict.
    """

    def __init__(self, test_mode):

        if test_mode is True:
            monitor_reltime = [0, 1, 2, 3, 4]
            resprate = [100, 100, 100, 100, 100]
            heartrate = [90, 90, 90, 90, 90]
            satrate = [80, 80, 80, 80, 80]
            resprate_lim = [100, 100, 100, 100, 100]
            heartrate_lim = [100, 100, 100, 100, 100]
            satrate_lim = [100, 100, 100, 100, 100]
            sensor_reltime = [100, 100, 100, 100, 100]
            accx = [2, 2, 2, 2, 2]
            accy = [2, 2, 2, 2, 2]
            accz = [2, 2, 2, 2, 2]
            gyrox = [2, 2, 2, 2, 2]
            gyroy = [2, 2, 2, 2, 2]
            gyroz = [2, 2, 2, 2, 2]

            dreamguard_plot.plot(monitor_reltime,
                                 resprate,
                                 heartrate,
                                 satrate,
                                 resprate_lim,
                                 heartrate_lim,
                                 satrate_lim,
                                 sensor_reltime,
                                 accx,
                                 accy,
                                 accz,
                                 gyrox,
                                 gyroy,
                                 gyroz)
            exit()

        else:
            try:
                monitor_import = dreamguard_import.Monitor()
                sensor_import = dreamguard_import.Sensor(monitor_import.folderpath)
                monitor = dreamguard_monitor.Monitor(monitor_import.unix_time,
                                                     monitor_import.reltime,
                                                     monitor_import.resprate,
                                                     monitor_import.heartrate,
                                                     monitor_import.satrate)
                sensor = dreamguard_sensor.Sensor(sensor_import.hourshex,
                                                  sensor_import.minuteshex,
                                                  sensor_import.secondshex,
                                                  sensor_import.millieshex,
                                                  sensor_import.accx1hex,
                                                  sensor_import.accx2hex,
                                                  sensor_import.accy1hex,
                                                  sensor_import.accy2hex,
                                                  sensor_import.accz1hex,
                                                  sensor_import.accz2hex,
                                                  sensor_import.gyrox1hex,
                                                  sensor_import.gyrox2hex,
                                                  sensor_import.gyroy1hex,
                                                  sensor_import.gyroy2hex,
                                                  sensor_import.gyroz1hex,
                                                  sensor_import.gyroz2hex)
                aligned = dreamguard_clock.Clock(monitor.timestamp,
                                                 monitor.reltime,
                                                 monitor.resprate,
                                                 monitor.heartrate,
                                                 monitor.satrate,
                                                 monitor.resprate_lim,
                                                 monitor.heartrate_lim,
                                                 monitor.satrate_lim,
                                                 sensor.timestamp,
                                                 sensor.reltime,
                                                 sensor.accx,
                                                 sensor.accy,
                                                 sensor.accz,
                                                 sensor.gyrox,
                                                 sensor.gyroy,
                                                 sensor.gyroz)
                dreamguard_plot.plot(aligned.monitor_reltime,
                                     aligned.resprate,
                                     aligned.heartrate,
                                     aligned.satrate,
                                     aligned.resprate_lim,
                                     aligned.heartrate_lim,
                                     aligned.satrate_lim,
                                     aligned.sensor_reltime,
                                     aligned.accx,
                                     aligned.accy,
                                     aligned.accz,
                                     aligned.gyrox,
                                     aligned.gyroy,
                                     aligned.gyroz)

            except Exception:
                # all errors should be catched by modules itself
                input("[INFO] Press ENTER to continue...")
