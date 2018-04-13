import requests
import time

from pprint import pprint

def main():
    lat = 33.699657
    lon = -86.635033
    api_key = "83942510644cc6a8bfceae5bed2e6ed8"
    api_call = f"https://api.darksky.net/forecast/{api_key}/{lat},{lon},{int(time.time())}?exclude=flags,alerts,currently,daily,minutely"
    r = requests.get(api_call)
    # print(r.status_code)
    # print(r.text)
    forecast = r.json()
    pprint(forecast)


if __name__ == '__main__': 
    main()
