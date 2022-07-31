from datetime import datetime as dt


def convert_to_iso_8601(data: dt) -> str:
    return data.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
