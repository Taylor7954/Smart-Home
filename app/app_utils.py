
import json

from models import EntryPoint, EntryPointHistory, Session

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

def get_water(home_id):
    """Get cost since the beginning of the month"""

def get_electricity(home_id):
    """Get cost since the beginning of the month"""
