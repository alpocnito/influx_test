import time
import sounddevice as sd
import influxdb_client

duration_sec = 2000

# Запись в influxDB
org = "mipt"
token='AxZQBiPLqGo7nkwQxuga16V_Ui8qY8livmN-TGKiqtTO3LOfAd3KNRslGYs4Eorcml1IgYlnwb8YtzM1jX22-Q=='
url="http://localhost:8086"
bucket = "bucket1"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

global_time = 0
def callback(indata, outdata, frames, _time, status):
    global global_time

    print('glob:', time.time() - global_time)
    points = []
    start = time.time()
    for val in indata:
        write_time = int(time.time() * 1_000_000_000)
        point = {
            "measurement": "a",
            "time": write_time,
            "tags": {
                "a": "i",
            },
            "fields": {
                "l": float(val[0]),
            }
        }
        points.append(point)
    with client.write_api() as write_api:
        write_api.write(bucket=bucket, org=org, record=points)
    print('proc:', time.time() - start)
    global_time = time.time()

with sd.Stream(channels=1, callback=callback, blocksize=44100):
    sd.sleep(int(duration_sec * 1000))
