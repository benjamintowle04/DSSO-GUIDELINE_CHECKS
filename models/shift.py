class Shift:
    def __init__(self, day, start_time, end_time, hours, station, group):
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.hours = hours
        self.station = station
        self.group = group

    def __str__(self):
        return (
            f"Day{self.day},"
            f"Hours:{self.hours}, "
            f"Start: {self.start_time},"
            f"End: {self.end_time},"
            f"Station: {self.station},"
            f"Group: {self.group}"
        )