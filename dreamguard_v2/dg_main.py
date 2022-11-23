### DATAGRABBER SCRIPT ###

# mandatory modules
module =        [
                "tkinter.filedialog",
                "tkinter",
                "math",
                "statistics",
                "csv",
                "numpy",
                "pandas",
                "matplotlib.pyplot",
                "threading",
                "time",
                "datetime",
                "serial"
                ]

module_name =   [
                "filedialog",
                "tk",
                "math",
                "stat",
                "csv",
                "np",
                "pd",
                "plt",
                "threading",
                "time",
                "datetime",
                "serial"
                ]


# dependencies
try:
    import dg_init
except Exception as err:
    print("[ERROR] ", err)
    input('Press ENTER key to exit...')
    exit()


# system and module check
dg_init.clear()
print(">>> DREAMGUARD STARTUP\n")
dg_init.system_check()
dg_init.install_modules(module, module_name)
dg_init.clear()


# dependencies
try:
    import dg_init
    import dg_global
    import dg_import
    import dg_sensor
    import dg_sensor_serial
    import dg_monitor
    import dg_calc
    import dg_diagram
    import dg_minmax
except Exception as err:
    print("[ERROR] ", err)
    input('Press ENTER key to exit...')
    exit()


# gui
def gui():
    print(">>> DREAMGUARD MANAGER")
    print("\n1 : SENSOR")
    print("2 : DIAGRAM")
    print("3 : MINMAX")
    print("4 : MINMAX CUSTOM")
    print("0 : EXIT")
    print("")
    while True:
        try:
            command = int(input("ENTER NUMBER TO SELECT COMMAND: "))
            if -1 < command < 4:
                break
        except:
            pass
    return command


# main function
def main():
    command = -1
    while command == -1:
        dg_init.clear()
        command = gui()
        if command == 1:
            dg_init.clear()
            if dg_global.flag == False: dg_sensor_serial.main_sensor()
        elif command == 2:
            dg_init.clear()
            if dg_global.flag == False: monitor_unix_time, monitor_reltime, resprate, heartrate, satrate = dg_import.monitor()
            if dg_global.flag == False: hertz, hourshex, minuteshex, secondshex, millsechex, accx1hex, accx2hex, accy1hex, accy2hex, accz1hex, accz2hex, gyrox1hex, gyrox2hex, gyroy1hex, gyroy2hex, gyroz1hex, gyroz2hex = dg_import.sensor()
            if dg_global.flag == False: monitor_timestamp, monitor_reltime_norm, resprate_norm, heartrate_norm, satrate_norm, resprate_lim, heartrate_lim, satrate_lim = dg_monitor.calc(monitor_unix_time, monitor_reltime, resprate, heartrate, satrate)
            if dg_global.flag == False: sensor_timestamp, sensor_reltime, accx, accy, accz, gyrox, gyroy, gyroz = dg_sensor.calc(hertz, hourshex, minuteshex, secondshex, millsechex, accx1hex, accx2hex, accy1hex, accy2hex, accz1hex, accz2hex, gyrox1hex, gyrox2hex, gyroy1hex, gyroy2hex, gyroz1hex, gyroz2hex)
            if dg_global.flag == False: monitor_reltime_norm, resprate_norm, heartrate_norm, satrate_norm, resprate_lim, heartrate_lim, satrate_lim, sensor_reltime, accx, accy, accz, gyrox, gyroy, gyroz = dg_calc.align_clock(hertz, monitor_timestamp, monitor_reltime_norm, resprate_norm, heartrate_norm, satrate_norm, resprate_lim, heartrate_lim, satrate_lim, sensor_timestamp, sensor_reltime, accx, accy, accz, gyrox, gyroy, gyroz)
            if dg_global.flag == False: dg_diagram.calc_plot(monitor_reltime_norm, resprate_norm, heartrate_norm, satrate_norm, resprate_lim, heartrate_lim, satrate_lim, sensor_reltime, accx, accy, accz, gyrox, gyroy, gyroz)
        elif command == 3:
            dg_init.clear()
            if dg_global.flag == False: dg_minmax.calc()
        elif command == 4:
            dg_init.clear()
        elif command == 0:
            dg_init.clear()
            exit()
        else:
            print(command)
            print("\n[ERROR] : unknown")
            input("\nPRESS ENTER TO EXIT")
            exit()
        command = -1
        dg_global.flag = False


# initial start
if __name__ == '__main__':
    main()