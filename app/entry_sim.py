
import time
import random

from datetime import datetime
# start from march 1st:

from models import Utilities, Session

# start on march 1
def main():

    session = Session()
    # prin

    curtime = datetime(2018, 2, 28).timestamp()

    while curtime < time.time():

        # if anything in db greater than now, continue
        match = session.query(Utilities)\
        .filter(Utilities.time > curtime)\
        .all()

        if match:
            print(match)
            continue

        # get day of week
        day = datetime.fromtimestamp(curtime).weekday()

        
        
        # increment day
        curtime += random.randint(0, 3600)
        print(time.time() - curtime)

    session.commit()
    print('done')

if __name__ == "__main__":
    main()