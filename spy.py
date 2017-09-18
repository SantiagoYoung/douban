import psutil
import sys
from datetime import datetime
from flask import Flask
from pymongo import MongoClient
import json
import time
import threading

app = Flask(__name__)
conn = MongoClient('localhost', 27017)
db = conn.monitor


def get_sys_info():
    cpu_usage_as_percentage = psutil.cpu_percent()
    per_cpu_percent = psutil.cpu_percent(percpu=True)
    total_memo = psutil.virtual_memory().total
    free_memo = psutil.virtual_memory().free
    used_memo = psutil.virtual_memory().used
    memo_usage_as_percentage = used_memo / total_memo * 100
    memo_free_as_percentage = free_memo / total_memo * 100
    swap_memo_as_percentage = psutil.swap_memory().percent
    disk_usage_as_percentage = psutil.disk_usage("/").percent
    user = psutil.users()[0].name
    boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    information = {
        'cpu_usage_as_percentage': cpu_usage_as_percentage,
        'per_cpu_percent': per_cpu_percent,
        'total_memo': total_memo,
        'free_memo': free_memo,
        'used_memo': used_memo,
        'memo_usage_as_percentage': memo_usage_as_percentage,
        'memo_free_as_percentage': memo_free_as_percentage,
        'swap_memo_ad_percentage': swap_memo_as_percentage,
        'disk_usage_as_percentage': disk_usage_as_percentage,
        'user': user,
        'boot_time': boot_time,
        # 'datetime': datetime.now().strftime("%H:%M:%S")
    }
    db.information.insert_one({"sys_info": information, 'datetime': datetime.now()})
    return


def task():
    while 1:
        time.sleep(5)
        get_sys_info()


@app.route("/")
def sys_info():
    get_sys_info()
    # information = db.information.find()
    information = db.information.find({"datetime": {"$lte": datetime.now()}})
    # information = db.information.find_one({"datetime": {"$lte": datetime.now().strftime("%H:%M:%S")}})['sys_info']
    # information = db.information.find()['sys_info']
    print(information)
    return json.dumps(information)

# monitor = threading.Thread(target=task())
# monitor.setDaemon(True)
app.run()


def get_all_process_info():
    all_process = list(psutil.process_iter())
    for i in list(psutil.process_iter()):
        print(i.cpu_percent(interval=1))
        print(i.memory_percent())


def get_temperature():
    temperatures = []
    if not hasattr(psutil, 'sensors_temperatures'):
        sys.exit("Platform not support.")
    temps = psutil.sensors_temperatures()
    if not temps:
        sys.exit("cant't read any temperature.")
    for name, entries in temps.items():
        print(name)
        for entry in entries:
            temperatures.append("    %-20s %s °C (high = %s °C, critical = %s °C)" % (
                entry.label or name, entry.current, entry.high,
                entry.critical))


