import subprocess
from time import sleep as ts

def start_service(service):
    subprocess.run(["sudo", "systemctl", "start", f"{service}"])

def stop_service(service):
    subprocess.run(["sudo", "systemctl", "stop", f"{service}"])


# start_services
start_service("serverTgBot")

while True:
    start_service("tgBot")

    ts(360)

    stop_service("tgBot")

