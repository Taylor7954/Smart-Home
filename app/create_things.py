
import time
import random

from datetime import datetime
# start from march 1st:

from models import ThingTracker, Session

session = Session()

def create_things(home_id):
    # create master bed
    session.add(
        ThingTracker(
            home_id=home_id,
            name="Keys"
        )
    )

    # create kid bed
    session.add(
        ThingTracker(
            home_id=home_id,
            name="Dog"
        )
    )

    session.commit()

# start on march 1
def main():

    # prin
    create_things(4)
    
    
    print('done')

if __name__ == "__main__":
    main()