import re
from jinja2 import pass_environment
import pandas as pd
from datetime import datetime
import pytz
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import requests
import json


def parse_str(x):
    if x is None:
        print("X : ", x)
        return "AAAAAAAAAAAAAAA"
    return x[1:-1]


def parse_datetime(x):
    try:
        dt = datetime.strptime(x[1:-7], '%d/%b/%Y:%H:%M:%S')
        dt_tz = int(x[-6:-3])*60+int(x[-3:-1])
        return dt.replace(tzinfo=pytz.FixedOffset(dt_tz))
    except:
        x = "[02/May/2021:03:20:40 +0700]"
        dt = datetime.strptime(x[1:-7], '%d/%b/%Y:%H:%M:%S')
        dt_tz = int(x[-6:-3])*60+int(x[-3:-1])
        return dt.replace(tzinfo=pytz.FixedOffset(dt_tz))


def parse_int(x):
    if x.isnumeric():
        return int(x)
    return x


data = pd.read_csv(
    'access.log',
    sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
    engine='python',
    na_values='-',
    header=None,
    usecols=[0, 3, 4, 5, 6, 7, 8],
    names=['ip', 'time', 'request', 'status',
           'size', 'referer', 'user_agent'],
    converters={'time': parse_datetime,
                'request': parse_str,
                'status': parse_int,
                'size': parse_int,
                'referer': parse_str,
                'user_agent': parse_str})


def get_ip():
    result = []
    ip_list = list(data.ip)
    for i in ip_list:
        print({"ip": i})
        result.append(get_location({"ip": i}))
    return result


def get_location(ip_address):
    ip_address = json.dumps(ip_address)
    print(f'https://ipapi.co/{ip_address}/json')
    response = requests.get(f'https://ipapi.co/{ip_address}/json').json()
    print(response)
    location_data = {
        "ip": ip_address["ip"],
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name"),
        "postal": response.get("postal"),
        "latitude": response.get("latitude"),
    }
    return location_data
