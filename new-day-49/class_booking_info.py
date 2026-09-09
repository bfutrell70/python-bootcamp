from dataclasses import dataclass


@dataclass
class ClassBookingInfo:
    """class for storing info for classes that are booked or waitlisted"""
    name: str
    date: str
    time: str
    waitlisted: bool