# Init script to check system, dependencies and modules


# check basic modules for initial startup
try:
    import os
    import sys
    import requests
    import subprocess
    import platform
    import importlib
except Exception as err:
    print("[ERROR] ", err, ". Should be a default package.")
    input('Press ENTER key to exit...')
    exit()


# check system
def system_check():
    try:
        if platform.system() == "Windows":
            proc = subprocess.Popen(["py", "--version"], stdout=subprocess.PIPE)
            version = ((proc.stdout.read()).decode('ascii')).strip()
            print("[INFO]", version, "found.")
        else:
            proc = subprocess.Popen(["python3", "--version"], stdout=subprocess.PIPE)
            version = ((proc.stdout.read()).decode('ascii')).strip()
            print("[INFO]", version, "found.")
    except Exception as e:
        print("[ERROR] ", e)
        input('Press ENTER key to exit...')
        exit()

    if platform.system() == "Darwin":
        print("[ERROR] macOS not supported.")
        input('Press ENTER key to exit...')
        exit()


# module installation
def install_modules(module, module_name):
    i = 0
    for x in module:
        try:
            globals()[module_name[i]] = importlib.import_module(x)
            print("[INFO] Import", x, "as", module_name[i])
        except Exception as e:
            print("[WARNING]", e, "Trying to install...\n")

            # install modules ("serial" is exception, because installed with "pyserial" but imported with "serial")
            if x == "serial":
                if platform.system() == "Windows":
                    subprocess.call(["py", "-m", "pip", "install", "pyserial"])
                else:
                    subprocess.call(["python3", "-m", "pip", "install", "pyserial"])
            else:
                if platform.system() == "Windows":
                    subprocess.call(["py", "-m", "pip", "install", x])
                else:
                    subprocess.call(["python3", "-m", "pip", "install", x])

            print("")
            try:
                globals()[module_name[i]] = importlib.import_module(x)
            except Exception as e:
                print("[ERROR] Installation of", x, "failed.")
                input("[INFO] Press ENTER to exit.")
                exit()
        i += 1


# check version
def check_version():
    version_web=((requests.get("https://raw.githubusercontent.com/geludwig/DraegerDreamGuard/main/dreamguard_v2/version")).text).partition('\n')[0]

    with open("version") as f:
        version_local = f.readline().strip('\n')
    f.close()

    if version_web > version_local:
        print("[ERROR] New update available. Please update.")
        input("[INFO] Press ENTER to exit.")
        exit()


# clear console
def clear():
    os.system('cls' if platform.system() =='Windows' else 'clear')