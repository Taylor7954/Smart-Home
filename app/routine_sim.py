
import time
import random

from datetime import datetime
# start from march 1st:

from models import Utilities, Session

def get_elec_const(day):

    use = []

    # 30 bulbs. On for 8 hours
    use += 8 * [60 * 20]

    # bath exhaust fan. On for 1 hour
    use += 2 * [30]

    # fridge. On for 24 hours
    use += [150 * 24]

    # MICROWAVE
    use += [1100 * (1/3)]

    # STOVE
    use += [3500 * (1/4)]

    # OVEN
    use += [4000 * (3/4)]

    # TV
    use += [636 * 4]
    use += [100 * 2]

    # HOT WATER HEATER. 4500w. 4 mins to heat 1 gal
    # showers. 16.25 gallons hot. 
    use += 2 * [4500 * (1/15) * 16.25]
    # baths. 19.5 gals hot
    use += 2 * [4500 * (1/15) * 19.5]
    # dishwasher. 6 gal hot. 4 loads
    use += 4 * [4500 * (1/15) * 6]
    # washer. 17 hot. 4 loads
    use += 4 * [4500 * (1/15) * 17]

    # DISHWASHER. 1800. 4 loads/week. 45 min
    use += 4 * [1800 * (3/4)]

    # WASHER. 500. 4 loads. 30 mins.
    use += 4 * [500 * (1/2)]

    # DRYER. 3000. 4 loads. 30 mins
    use += 4 * [3000 * (1/2)]

    if day > 5:

        # 30 bulbs. On from 05 to 22 +- 1
        use += 8 * [60 * 20]

        # add extra usage for weekend
        # MICROWAVE
        use += [1100 * (1/6)]

        # STOVE
        use += [3500 * (1/4)]
        
        # OVEN
        use += [4000 * (1/4)]

        # TV
        use += [636 * 4]
        use += [100 * 2]

        # HOT WATER HEATER. 4500w. 4 mins to heat 1 gal
        # showers. 16.25 gallons hot. 
        use += [4500 * (1/15) * 16.25]
        # baths. 19.5 gals hot
        use += [4500 * (1/15) * 19.5]

    return use

def get_HVAC_use(start: list, target):
    """Get the use of the HVAC over the day from the temp"""

def get_water_const(day):
    """get the useage of water for day"""

    use = []

    # BATHS
    # shower
    use += 2 * [25]
    # baths
    use += 2 * [25]

    # DISHWASER
    use += 4 * [6]

    # WASHER
    use += 4 * [20]

    if day > 5:
        # BATHS
        # shower
        use += [25]
        #baths
        use += [25]

    return use

# start on march 1
def main():

    session = Session()
    # prin

    curtime = datetime(2018, 2, 28).timestamp()

    while curtime < time.time():

        # if anything in db greater than now, continue
        match = session.query(Utilities)\
        .filter(Utilities.time > curtime)\
        .filter(Utilities.home_id == 4)\
        .all()

        if match:
            print(match)
            continue

        # get day of week
        day = datetime.fromtimestamp(curtime).weekday()

        # for each cost, put into db with random time during day
        elec = get_elec_const(day)

        # print((elec))
        for _e in elec:
            new_util = Utilities(
                utility_type="electricity",
                usage=_e,
                time=curtime + random.randint(0, 86399),
                home_id=4
            )

            # print('added', _e)
            session.add(new_util)

        water = get_water_const(day)

        for _w in water:
            new_util = Utilities(
                utility_type="water",
                usage=_w,
                time=curtime + random.randint(0, 86399),
                home_id=4
            )

            session.add(new_util)

        # increment day
        curtime += 86400
        print(time.time() - curtime)

    session.commit()
    print('done')

if __name__ == "__main__":
    main()