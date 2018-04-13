
import time
import random

from datetime import datetime
# start from march 1st:

def get_elec_const(day):

    cost = []

    # 30 bulbs. On from 05 to 22 +- 1
    cost += [(60 * 30) * (17)]

    # bath exhaust fan. On for 1 hour
    cost += [(30 * 2) * 1]

    # fridge. On for 24 hours
    cost += [150 * (24 * 1)]

    # MICROWAVE
    cost += [1100 * (1/3)]

    # STOVE
    cost += [3500 * (1/4)]

    # OVEN
    cost += [4000 * (3/5)]

    # TV
    cost += [636 * 4]
    cost += [100 * 2]

    # HOT WATER HEATER. 4500w. 4 mins to heat 1 gal
    # showers. 16.25 gallons hot. 
    cost += [2 * (4500 * (1/15) * 16.25)]
    # baths. 19.5 gals hot
    cost += [2 * (4500 * (1/15) * 19.5)]

    if day > 5:
        # add extra usage for weekend
        # MICROWAVE
        cost += [1100 * (1/6)]

        # STOVE
        cost += [3500 * (1/4)]
        
        # OVEN
        cost += [4000 * (1/4)]

        # TV
        cost += [636 * 4]
        cost += [100 * 2]

        # HOT WATER HEATER. 4500w. 4 mins to heat 1 gal
        # showers. 16.25 gallons hot. 
        cost += [4500 * (1/15) * 16.25]
        # baths. 19.5 gals hot
        cost += [4500 * (1/15) * 19.5]

    return cost

    

def get_HVAC(temp: list):
    """Get the cost of the HVAC over the day from the temp"""

def get_water(day):
    pass

# start on march 1
def main():
    curtime = datetime(2018, 3, 1).timestamp()

    while curtime < time.time():

        # get day of week
        day = datetime.fromtimestamp(curtime).weekday()

        # for each cost, put into db with random time during day
        elec = get_elec_const(day)
        print(elec)
        print(sum(elec) / 1000 * .12)

        # increment day
        curtime += 86400

if __name__ == "__main__":
    main()