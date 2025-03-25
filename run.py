import os
import subprocess
import sys
import threading
import time


# Execute a Python script
def execute(path):
    subprocess.run(["python", path])


if len(sys.argv) > 1:
    if sys.argv[1] == "install" or sys.argv[1] == "i":
        try:
            os.system("playwright install chromium")
        except Exception as e:
            print(e)
            pass


# Execute a Python script
thred1 = threading.Thread(target=execute, args=("scrappers/scrapper_cotacao.py",))
thred1.start()
time.sleep(15)
thred2 = threading.Thread(target=execute, args=("scrappers/scrapper_clima.py",))
thred2.start()
