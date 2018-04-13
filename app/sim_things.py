
import time
import random

from datetime import datetime
# start from march 1st:
from models import Room, ThingTracker, Session

session = Session()

def run_sim(home_id):

    while True:

        # print('enter')

        match = session.query(ThingTracker)\
        .filter(ThingTracker.home_id == home_id)\
        .all()

        for thing in match:

            rm_match = session.query(Room)\
            .filter(Room.home_id == home_id)\
            .all()

            rand_entry = random.choice(rm_match)
            # print('here')
            if random.random() > 0.1:
                # print('room')
                thing.room_id = rand_entry.id
            else:
                # print('none')
                thing.room_id = None

        # print(rand_entry.is_open)

        # now update the histor

        session.commit()
        
# start on march 1
def main():

    # prin
    run_sim(4)

if __name__ == "__main__":
    main()