
import time
import random

from datetime import datetime
# start from march 1st:

from models import Room, EntryPoint, Session

session = Session()

def create_house(home_id):
    # create master bed
    session.add(
        Room(
            home_id=home_id,
            name="Master"
        )
    )

    # create kid bed
    session.add(
        Room(
            home_id=home_id,
            name="Guest Bed"
        )
    )

    # create kid bed
    session.add(
        Room(
            home_id=home_id,
            name="Kids"
        )
    )

    # create 16 windows
    for _n in range(16):
        session.add(
            EntryPoint(
                home_id=home_id,
                name=f'Window{_n}',
                type='window',
                is_open=False
            )
        )

    # create 3 doors
    for _n in range(3):
        session.add(
            EntryPoint(
                home_id=home_id,
                name=f'Door{_n}',
                type='door',
                is_open=False
            )
        )

    session.commit()

# start on march 1
def main():

    # prin
    create_house(4)
    
    
    print('done')

if __name__ == "__main__":
    main()