#!/usr/bin/env python
import serial
import ConfigParser
#import mysql.connector as mariadb
from influxdb import InfluxDBClient
#import memcache

# Read the configuration file
config = ConfigParser.ConfigParser()
config.read('config.ini')

# Serial Parameters
baudrate = config.getint('serial', 'baudrate')
serial_port = config.get('serial' ,'port')

# Internal variables
valid_row = False
serial_input = []
line = []
row = []
juice_vars_raw = []
juice_vars = {
    'id': None,
    'voltage': None,
    'frequency': None,
    'amps': None,
    'temperature': None,
    'state': None,
    'energy': None,
}


# Open some stuff
port = serial.Serial(serial_port, baudrate)  # open se'rial port

influx = InfluxDBClient(config.get('influx', 'host'),
                        config.get('influx', 'port'),
                        config.get('influx', 'user'),
                        config.get('influx', 'password'),
                        config.get('influx', 'db'),
                        )

# Functions
def insert_into_influx(vars, raw):
    if vars['id'] is not None:
        try:
            json_body = [
            {
               "measurement": "JuiceBox",
                "tags": {
                    "id": vars['id']
                },
                "fields": {
                    "voltage": vars['voltage'],
                    "frequency": vars['frequency'],
                    "amps": vars['amps'],
                    "temperature": vars['temperature'],
                    "state": vars['state'],
                    "energy": vars['energy'],
                    "raw": str(raw),
                }
            }
            ]
            print json_body
            influx.write_points(json_body)
        except Exception, e:
            print e

while True:
    for c in port.read():
        serial_input.append(c)
        line = ''.join(str(v) for v in serial_input)
        if c == '\n':
            serial_input = []
            if line.startswith(config.get('juicebox', 'id')):
                row = line.split(':')
                juice_vars_raw = row[1].split(',')
                juice_vars = {
                    'id': None,
                    'voltage': None,
                    'frequency': None,
                    'amps': None,
                    'temperature': None,
                    'state': None,
                    'energy': None,
                }
                juice_vars['id'] = row[0]
                for item in juice_vars_raw:
                    if(item.startswith('V')):
                        juice_vars['voltage'] = int(item[1:])
                        valid_row = True
                    if(item.startswith('f')):
                        juice_vars['frequency'] = int(item[1:])
                        valid_row = True
                    if(item.startswith('A')):
                        juice_vars['amps'] = int(item[1:])
                        valid_row = True
                    if(item.startswith('E')):
                        juice_vars['energy'] = int(item[1:])
                        valid_row = True
                    if(item.startswith('T')):
                        juice_vars['temperature'] = int(item[1:])
                        valid_row = True
                    if(item.startswith('S')):
                        juice_vars['state'] = int(item[1:])
                        valid_row = True
                if(valid_row):
                   insert_into_influx(juice_vars,line)
                   valid_row = False
                print "Raw:"
                print line
