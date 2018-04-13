
import time
import random

from datetime import datetime
# start from march 1st:
from app_utils import update_entry_points
from models import Room, EntryPoint, EntryPointHistory, Session

session = Session()

def run_sim(home_id):

    while True:

        time_range = time.time() - datetime(2018, 3, 1).timestamp()

        match = session.query(EntryPoint)\
        .filter(EntryPoint.home_id == home_id)\
        .all()

        rand_entry = random.choice(match)

        # print(rand_entry.is_open)

        rand_entry.is_open = not rand_entry.is_open

        map(lambda x: not x.is_open, [d for d in match if d.is_open and d.type == 'door'])

        # now update the history
        session.add(
            EntryPointHistory(
                home_id=home_id,

            )
        )

        session.commit()

        rand_time = random.random() * time_range
        update_entry_points(home_id, rand_time)
        # print(match)
        print('updated history')
        

# start on march 1
def main():

    # prin
    run_sim(4)

if __name__ == "__main__":
    main()