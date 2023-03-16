'''Calculate vaues for sensor data.'''


if __name__ == '__main__':
    print(f">>> DREAMGUARD STARTUP\n")
    print(f"[ERROR] Start program with '_main.py'")
    exit()


import traceback
import datetime
import threading
import dreamguard_global


class Sensor:
    """Process sensor data with multithreading to reduce calculation time.
    Return:     self.reltime
                self.timestamp
                self.accx
                self.accy
                self.accz
                self.gyrox
                self.gyroy
                self.gyroz
    """

    def __init__(self, hourshex, minuteshex, secondshex, millieshex,
                 accx1hex, accx2hex, accy1hex, accy2hex, accz1hex, accz2hex,
                 gyrox1hex, gyrox2hex, gyroy1hex, gyroy2hex, gyroz1hex, gyroz2hex):
        hertz = dreamguard_global.HERTZ

        # Calc relative time
        def calc_reltime():
            """calculate relative time
            create global reltime list of int
            """
            try:
                global reltime
                length = len(millieshex)
                timesensorfloat = []
                calcsec = 0
                calcmill = 0
                intervall = 1000/hertz
                i = 0
                # calc ms and add one second after overflow
                # -> [..., 961, 1000, 1038, ... 1961, 2000, 2038, ...]
                while i < length:
                    if calcmill >= 999:
                        calcmill = 0
                        calcsec = calcsec + 1000
                    calctime = calcsec + calcmill
                    timesensorfloat.append(calctime)
                    calcmill = calcmill + intervall
                    i = i+1
                    # progress = 100 / (length / i)
                    # print('[INFO] Progress:', '%.1f' % progress, '%', end='\r') # progress bar
                reltime = [int(x) for x in timesensorfloat]
            except:
                print(f"[ERROR] {traceback.format_exc()}")
                raise

        # calc timestamp
        def calc_timestamp():
            """calculate datetime object timestamp"""
            try:
                global timestamp
                timestamp = []
                millisec_unix = []

                def convert_hex(arrayhex):
                    global listclock
                    listclock = []
                    for x in arrayhex:
                        x = int(str(x), 16)
                        listclock.append(x)
                    return listclock

                # convert hex to timestamp
                hours = convert_hex(hourshex)
                hours = [('%02d' % (x,)) for x in hours]
                minutes = convert_hex(minuteshex)
                minutes = [('%02d' % (x,)) for x in minutes]
                seconds = convert_hex(secondshex)
                seconds = [('%02d' % (x,)) for x in seconds]
                millisec = convert_hex(millieshex)

                # milliseconds (0, 1, 2, 3, ... 25, 0, 1, ...) to milliseconds with leading zeros
                # leading zeros needed for conversion
                #   timestamp.append(datetime.datetime.strptime(temp,'%H:%M:%S.%f')) later on
                # otherwise 38ms == 380ms
                for x in millisec:
                    temp = int(x * (1000/hertz))
                    if temp == 0:
                        temp = "000"
                    elif temp < 100:
                        temp = "0" + str(temp)
                    millisec_unix.append(temp)

                # convert string to datetime obj timestamp
                for hours, minutes, seconds, millisec_unix in zip(hours, minutes, seconds, millisec_unix):
                    temp = '{}:{}:{}.{}'.format(hours, minutes, seconds, millisec_unix)
                    timestamp.append(datetime.datetime.strptime(temp, '%H:%M:%S.%f'))

            except:
                print(f"[ERROR] {traceback.format_exc()}")
                raise

        # ACCELEROMETER
        # X
        def calc_acc_x():
            """zip two hex strings
            calculate correct values of x-axis of acccelerometer
            """
            try:
                global accx
                arrayint = []
                accxhex = [str(m)+str(n) for m, n in zip(accx1hex, accx2hex)]
                # zip two hex strings together to form a hex string with 4 dgt
                for x in accxhex:
                    x = int(str(x), 16)
                    if x > 32767:
                        x -= 65536
                    arrayint.append(x)
                # convert signed to correct G-Values
                accx = [x / 16384 for x in arrayint]
            except:
                print(traceback.format_exc())
                raise

        # Y
        def calc_acc_y():
            """zip two hex strings
            calculate correct values of y-axis of acccelerometer
            """
            try:
                global accy
                arrayint = []
                accyhex = [str(m)+str(n) for m, n in zip(accy1hex, accy2hex)]
                for x in accyhex:
                    x = int(str(x), 16)
                    if x > 32767:
                        x -= 65536
                    arrayint.append(x)
                accy = [x / 16384 for x in arrayint]
            except:
                print(f"[ERROR] {traceback.format_exc()}")
                raise

        # Z
        def calc_acc_z():
            """zip two hex strings
            calculate correct values of z-axis of acccelerometer
            """
            try:
                global accz
                arrayint = []
                acczhex = [str(m)+str(n) for m, n in zip(accz1hex, accz2hex)]
                for x in acczhex:
                    x = int(str(x), 16)
                    if x > 32767:
                        x -= 65536
                    arrayint.append(x)
                accz = [x / 16384 for x in arrayint]
            except:
                print(f"[ERROR] {traceback.format_exc()}")
                raise

        # GYRO
        # X
        def calc_gyro_x():
            """zip two hex strings
            calculate correct values of x-axis of gyroscope
            """
            try:
                global gyrox
                arrayint = []
                gyroxhex = [str(m)+str(n) for m, n in zip(gyrox1hex, gyrox2hex)]
                for x in gyroxhex:
                    x = int(str(x), 16)
                    if x > 32767:
                        x -= 65536
                    arrayint.append(x)
                gyrox = [x / 132 for x in arrayint]
            except:
                print(f"[ERROR] {traceback.format_exc()}")
                raise

        # Y
        def calc_gyro_y():
            """zip two hex strings
            calculate correct values of y-axis of gyroscope
            """
            try:
                global gyroy
                arrayint = []
                gyroyhex = [str(m)+str(n) for m, n in zip(gyroy1hex, gyroy2hex)]
                for x in gyroyhex:
                    x = int(str(x), 16)
                    if x > 32767:
                        x -= 65536
                    arrayint.append(x)
                gyroy = [x / 132 for x in arrayint]
            except:
                print(f"[ERROR] {traceback.format_exc()}")
                raise

        # Z
        def calc_gyro_z():
            """zip two hex strings
            calculate correct values of z-axis of gyroscope
            """
            try:
                global gyroz
                arrayint = []
                gyrozhex = [str(m)+str(n) for m, n in zip(gyroz1hex, gyroz2hex)]
                for x in gyrozhex:
                    x = int(str(x), 16)
                    if x > 32767:
                        x -= 65536
                    arrayint.append(x)
                gyroz = [x / 132 for x in arrayint]
            except:
                print(f"[ERROR] {traceback.format_exc()}")
                raise

        # MULTITHREADING
        # threadcount = threading.active_count()
        print(f"[INFO] Starting multithreaded calculations. This could take some time.")
        try:
            thread1 = threading.Thread(target=calc_reltime)
            thread2 = threading.Thread(target=calc_timestamp)
            thread3 = threading.Thread(target=calc_gyro_x)
            thread4 = threading.Thread(target=calc_gyro_y)
            thread5 = threading.Thread(target=calc_gyro_z)
            thread6 = threading.Thread(target=calc_acc_x)
            thread7 = threading.Thread(target=calc_acc_y)
            thread8 = threading.Thread(target=calc_acc_z)
            thread1.start()
            thread2.start()
            thread3.start()
            thread4.start()
            thread5.start()
            thread6.start()
            thread7.start()
            thread8.start()
            thread1.join()
            thread2.join()
            thread3.join()
            thread4.join()
            thread5.join()
            thread6.join()
            thread7.join()
            thread8.join()

            self.reltime = reltime
            self.timestamp = timestamp
            self.accx = accx
            self.accy = accy
            self.accz = accz
            self.gyrox = gyrox
            self.gyroy = gyroy
            self.gyroz = gyroz
        except:
            print(f"[ERROR] {traceback.format_exc()}")
            raise
