
import json
from datetime import datetime

from app.models import EntryPoint, EntryPointHistory, Utilities, Session

session = Session()

def update_entry_points(home_id, timestamp):

    match = session.query(EntryPoint)\
    .filter(EntryPoint.home_id == home_id)\
    .filter(EntryPoint.is_open == True)\
    .all()

    opened = [[ep.id, ep.type] for ep in match]

    json_str = json.dumps(opened)

    session.add(
        EntryPointHistory(
            time=timestamp,
            home_id=home_id,
            open_points=json_str
        )
    )

    session.commit()

def get_water(home_id, year, month):
    """Get cost since the beginning of the month"""

    # get the timestamp of the month and month + 1
    cur_month = datetime(year, month, 1).timestamp()

    # set increment year if the month was december
    month += 1
    if month == 12:
        year += 1
        month = 1
    next_month = datetime(year, month, 1).timestamp()
    #print(cur_month, next_month)

    # base cost of bill
    base_charge = 34.48
    # 748 gallons in a ccf
    CCF = 748

    gal_usage = 0
    ccf_multiplier = 2.43

    match = session.query(Utilities)\
    .filter(Utilities.home_id == home_id)\
    .filter(Utilities.utility_type == 'water')\
    .filter(Utilities.time >= cur_month)\
    .filter(Utilities.time <= next_month)\
    .all()

    for _w in match:
        gal_usage += _w.usage
    
    # print(gal_usage)

    ccf_usage = gal_usage / CCF

    if ccf_usage >= 4:
        ccf_multiplier = 2.87
    elif ccf_usage > 15:
        ccf_multiplier = 4.29

    usage_charge = ccf_usage * ccf_multiplier + base_charge

    return usage_charge

def get_electricity(home_id):
    """Get cost since the beginning of the month"""
	
if __name__ == '__main__':
    water = get_water(4, 2018, 3)