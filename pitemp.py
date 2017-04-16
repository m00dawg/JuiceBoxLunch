#!/usr/bin/env python
# Grab Pi's GPU and CPU temperatures and chuck them into InfluxDB

import ConfigParser
import subprocess
from influxdb import InfluxDBClient

# Read the configuration file
config = ConfigParser.ConfigParser()
config.read('config.ini')

influx = InfluxDBClient(config.get('influx', 'host'),
                        config.get('influx', 'port'),
                        config.get('influx', 'user'),
                        config.get('influx', 'password'),
                        config.get('influx', 'db'),
                        )

cpu_temp = subprocess.check_output(["cat", "/sys/class/thermal/thermal_zone0/temp"])
gpu_temp_raw = subprocess.check_output(["vcgencmd", "measure_temp"])
gpu_temp = int(round(float(gpu_temp_raw.split("=")[1].split("'")[0])))

# Insert CPU Metric
json_body = [
{
    "measurement": "DeviceTemperatures",
    "tags": {
        "device": "JuiceDawg",
        "sensor": "CPU"
    },
    "fields": {
        "temperature": int(cpu_temp) / 1000,
    }
}
]
influx.write_points(json_body)

# Insert GPU Metric
json_body = [
{
    "measurement": "DeviceTemperatures",
    "tags": {
        "device": "JuiceDawg",
        "sensor": "GPU"
    },
    "fields": {
        "temperature": int(gpu_temp),
    }
}
]
influx.write_points(json_body)
