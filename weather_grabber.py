"""
Gets one month of info from the weather API
"""

# ===STD IMPORTS
from datetime import datetime

# ===PIP IMPORTS
import requests

from sqlalchemy.dialects.postgresql import insert

# ===LOCAL IMPORTS
from app.models import Forecast, engine, Session

def get_weather(timestamp, lat, lon):
    """Get weather at timestamp, lat, lon"""

    api_key = "83942510644cc6a8bfceae5bed2e6ed8"
    api_call = f"https://api.darksky.net/forecast/{api_key}/{lat},{lon},{int(timestamp)}?exclude=flags,alerts,currently,daily,minutely"
    r = requests.get(api_call)
    # print(r.status_code)
    # print(r.text)
    return r.json()

def filter_weather(data):
    """strip weather data"""

    data = data['hourly']['data']
    # print(data)
    for _x in data:
        # pop all except for interested keys
        keys = ('time', 'summary', 'precipIntensity', 'precipProbability', 'precipType', 'temperature')

        _x_keys = list(_x.keys())
        for key in _x_keys:
            if key not in keys:
                _x.pop(key)

    return data

# days grab in 48 hour chunks. Grab only 15 days
march = datetime(2018, 3, 1).timestamp()
print(march)

weather = get_weather(march, 33.699657, -86.635033)
weather = filter_weather(weather)
print(weather)

# select on lat, lon, time
values = {

}

session = Session()

stmt = insert(Forecast.__tablename__, values=values).values(
    id='some_id',
    data='inserted value'
    )

do_update_stmt = stmt.on_conflict_do_update(
    index_elements=['id'],
    set_=dict(data='updated value')
    )
session.execute(do_update_stmt)