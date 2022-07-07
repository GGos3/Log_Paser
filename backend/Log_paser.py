from datetime import datetime
import pandas as pd
import pytz
import requests
import glob


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


files = glob.glob("log_sample/access.*")

for i, filename in enumerate(files):
    data = pd.read_csv(
        filename,
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


def get_location():
    result = []
    ip_list = list(data.ip)
    request_headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0;Win64; x64)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98\
    Safari/537.36'), }

    for i in ip_list:
        print(f'https://ipapi.co/{i}/json')
        response = requests.get(
            f'https://ipapi.co/{i}/json', headers=request_headers).json()
        location_data = {
            "ip": i,
            "city": response.get("city"),
            "region": response.get("region"),
            "country": response.get("country_name"),
            "postal": response.get("postal"),
            "latitude": response.get("latitude"),
        }
        result.append(location_data)

    return result


def get_request():
    return data.request
