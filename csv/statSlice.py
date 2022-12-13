from datetime import datetime
from enum import Enum


class StatInterval(Enum):
    minutes_15 = 0
    minutes_30 = 1
    daily = 2


class AWSStatSlice:
    """Represents a single row of a CSV file for AWS Connect."""

    CHANNEL_TYPE: str
    TIMESTAMP: datetime
    INTERVAL: StatInterval
    INCOMING_CONTACT_VOLUME: int  # number of inbound, transfer, and callback contacts
    AVERAGE_HANDLE_TIME: int  # in seconds
    CONTACTS_HANDLED: int  # number of inbound, transfer, and callback contacts _handled_
