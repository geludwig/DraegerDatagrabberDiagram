'''Init module with variuos system, os, and module check functions

Pylint error: "Redefining name 'err' from outer scope" makes not really sense for me,
because I want to redefine it and not use different variables every time an error message is printed.
'''


# https://www.daniweb.com/programming/software-development/threads/420592/pass-arguments-to-import-module-a
if __name__ == '__main__':
    print(">>> DREAMGUARD STARTUP\n")
    print("[ERROR] Start program with '_main.py'")
    exit()


# check basic modules for init module
try:
    import os
    import subprocess
    import platform
    import importlib
    import time
except Exception as err:
    print(f"[ERROR] {err}. Should be a default package.")
    input('Press ENTER key to exit...')
    exit()


# check system
def system_check():
    '''Checks operating system and python version if it is installed in PATH'''
    try:
        if platform.system() == "Windows":
            proc = subprocess.Popen(["py", "--version"], stdout=subprocess.PIPE)
            version = ((proc.stdout.read()).decode('ascii')).strip()
            print(f"[INFO] {version} found.")
        else:
            proc = subprocess.Popen(["python3", "--version"], stdout=subprocess.PIPE)
            version = ((proc.stdout.read()).decode('ascii')).strip()
            print(f"[INFO] {version} found.")
    except Exception as err:
        print(f"[ERROR] {err}")
        input('Press ENTER key to exit...')
        exit()

    if platform.system() == "Darwin":
        print(f"[ERROR] macOS not supported.")
        input('Press ENTER key to exit...')
        exit()


# automatic module installation
def install_modules(module, module_name):
    '''Automatic module installation'''
    i = 0
    install_flag = False

    # check if pip available and install if not (only linux)
    if platform.system() == "Linux":
        try:
            proc = subprocess.Popen(["pip", "--version"], stdout=subprocess.PIPE)
            version = ((proc.stdout.read()).decode('ascii')).strip()
            print(f"[INFO] {version} found.")
        except Exception as err:
            print(f"[WARNING] {err}. Trying to install...")
            subprocess.call(["sudo", "apt-get", "install", "python3-pip"])
            try:
                proc = subprocess.Popen(["pip", "--version"], stdout=subprocess.PIPE)
                version = ((proc.stdout.read()).decode('ascii')).strip()
                print(f"[INFO] {version} found.")
            except Exception as err:
                print(f"[ERROR] {err}. Try to install it manually.")
                input("[INFO] Press ENTER to exit.")
                exit()
    

    # install packages listed in "_main"
    for x in module:
        try:
            globals()[module_name[i]] = importlib.import_module(x)
            print(f"[INFO] Import {x} as {module_name[i]}")
        except Exception as err:
            print(f"[WARNING] {err}. Trying to install...")

            # package install exceptions, mostly where install name != import name
            if x == "matplotlib.pyplot" or x == "tkinter":

                if x == "matplotlib.pyplot":
                    if platform.system() == "Windows":
                        subprocess.call(["py", "-m", "pip", "install", "matplotlib"])
                    else:
                        subprocess.call(["python3", "-m", "pip", "install", "matplotlib"])

                if x == "tkinter":
                    if platform.system() == "Linux":
                        subprocess.call(["sudo", "apt-get", "install", "python3-tk", "-y"])

            # other packages
            else:
                if platform.system() == "Windows":
                    subprocess.call(["py", "-m", "pip", "install", x])
                else:
                    subprocess.call(["python3", "-m", "pip", "install", x])

            install_flag = True
        i += 1

    if install_flag == True:
        print("\n[INFO] Please restart python script.")
        print("[INFO] If error persists, please install package manually.")
        input("[INFO] Press ENTER to exit.")
        exit()


# timer
def timer():
    '''Timer to wait amount x to show initial startup message.'''
    i = 0
    wait = 2
    print(f"")
    while i < wait:
        print(f" Starting in {wait - i} seconds", end='\r')
        i += 1
        time.sleep(1)


# clear console
def clear():
    '''Clear command for console'''
    os.system('cls' if platform.system() == 'Windows' else 'clear')
