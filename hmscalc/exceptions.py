class HMSTimeError(Exception):
    pass


class InvalidTimeFormatError(HMSTimeError):
    def __init__(self, time_str: str):
        super().__init__(f"Invalid time format: '{time_str}'")

class NotTimeStringError(HMSTimeError):
    def __init__(self, value):
        super().__init__(f"Time input must be a string, got: {type(value).__name__}")