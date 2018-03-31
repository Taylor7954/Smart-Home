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
        # keys = ('time', 'summary', 'precipIntensity', 'precipProbability', 'precipType', 'temperature')
        keys = ('time', 'precipIntensity', 'precipProbability', 'precipType', 'temperature')

        _x_keys = list(_x.keys())
        for key in _x_keys:
            if key not in keys:
                _x.pop(key)

    return data

def main():
    # create a new session before executing inserts
    session = Session()

    # days grab in 24 hour chunks
    for day in range(1, 32):
        # get weather for month of march
        march = datetime(2018, 3, day).timestamp()
        # print(march)

        lat = 33.699657
        lon = -86.635033
        weather = get_weather(march, lat, lon)
        weather = filter_weather(weather)
        # print(weather)

        # select on lat, lon, time
        # make a new Forecast
        for w in weather:
            # print(**w)
            new_forecast = Forecast(
                latitude=lat,
                longitude=lon,
                **w
            )

            # match on lat, lon, time
            match = session.query(Forecast)\
            .filter(Forecast.latitude==lat)\
            .filter(Forecast.longitude==lon)\
            .filter(Forecast.time==w['time'])\
            .all()
                

            # if there were no matching records, insert
            if not match:
                print(f'Added: {new_forecast}')
                session.add(new_forecast)

        # save changes
    session.commit()
    print('DONE')

if __name__ == '__main__':
    main()