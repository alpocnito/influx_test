import time
import sounddevice as sd
import influxdb_client
import numpy as np

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

saved = []
global_time = 0
def callback(indata, outdata, frames, _time, status):
    global saved, global_time

    print('glob:', time.time() - global_time)
    start = time.time()
    left_data = client.query_api().query_stream(
        f'from(bucket:"{bucket}") |> range(start: -1s) '
        f'|> filter(fn: (r) => r["_measurement"] == "a") '
        f'|> filter(fn: (r) => r["_field"] == "l") '
        f'|> map(fn: (r) => ({{r with _value: r._value * 20.0}}))'
    )
    for point in left_data:
        # print(point.get_time().timestamp()*1_000_000_000)
        saved.append([point.get_value()])

    if len(saved) != 44100:
        add_len = 44100 - len(saved)
        if add_len > 0:
            print(f'{add_len = }')
            time.sleep(1)
        saved = [*([[0]] * add_len), *saved]
        outdata[:] = np.array(saved[:44100])
        saved = saved[44100:]
        # print("read:", int(time.time()))
    print('proc:', time.time() - start)
    global_time = time.time()

with sd.Stream(channels=1, callback=callback, blocksize=44100):
    sd.sleep(int(duration_sec * 1000))
