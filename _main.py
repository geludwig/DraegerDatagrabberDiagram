"""
Main module.

Sources are listed inside code.
Additional sources:
    Thomas Theis. Einstieg in Python. Rheinwerk Verlag, 2022 Bonn.
"""

# complete list of modules needed
module =        [
                "pathlib",
                "traceback",
                "math",
                "datetime",
                "threading",
                "pandas",
                "numpy",
                "matplotlib.pyplot",
                "tkinter",
                "tkinter.filedialog"

                ]

module_name =   [
                "pathlib",
                "traceback",
                "math",
                "datetime",
                "threading",
                "pd",
                "np",
                "plt",
                "tk",
                "filedialog"
                ]


# Check if init and global module is present
try:
    import dreamguard_global
    import dreamguard_init
except Exception as err:
    print(f"[ERROR] {err}")
    input('Press ENTER key to exit...')
    exit()


# Init process
dreamguard_init.clear()
print(f">>> DREAMGUARD STARTUP\n")
dreamguard_init.system_check()
dreamguard_init.install_modules(module, module_name)
dreamguard_init.timer()


# Check if all other modules are present
try:
    import dreamguard_diagram
    import dreamguard_import
    import dreamguard_monitor
    import dreamguard_sensor
    import dreamguard_clock
    import dreamguard_plot
except Exception as err:
    print(f"[ERROR] {err}")
    input('Press ENTER key to exit...')
    exit()


def gui():
    """Prints GUI and selects menu command."""
    while True:
        try:
            dreamguard_init.clear()
            print(f">>> DREAMGUARD MANAGER")
            print(f"\n1 : DIAGRAM")
            print(f"0 : EXIT")
            command = int(input("\nENTER NUMBER TO SELECT COMMAND: "))
            if -1 < command < 2:
                break
        except:
            pass
    return command


def main():
    """Main function."""
    test_mode = False
    command = -1

    while True:
        command = gui()
        dreamguard_init.clear()

        if command == 1:
            dreamguard_diagram.Diagram(test_mode)
        if command == 0:
            exit()

        command = -1


if __name__ == '__main__':
    main()
