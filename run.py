import subprocess
import threading
import time


# Execute a Python script
def execute(path):
    subprocess.run(["Python", path])


# Execute a Python script
thred1 = threading.Thread(target=execute, args=("scrappers/scrapper_cotacao.py",))
thred1.start()
time.sleep(15)
thred2 = threading.Thread(target=execute, args=("scrappers/scrapper_clima.py",))
thred2.start()
