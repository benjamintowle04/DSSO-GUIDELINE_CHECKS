from models.shift import Shift
class Employee:
    def __init__(
        self,
        last_name,
        first_name,
        external_id,
        shift_count,
        hours,
        supervisor,
        missing_reqs,
        schedule,
        schedule_valid,
        notes,
    ):
        self.last_name = last_name
        self.first_name = first_name
        self.external_id = external_id
        self.shift_count = shift_count
        self.hours = hours
        self.supervisor = supervisor
        self.missing_reqs = missing_reqs
        self.schedule = schedule
        self.schedule_valid = schedule_valid
        self.notes = notes

    def __str__(self):
        return (
            f"Employee({self.first_name} {self.last_name}, "
            f"ID: {self.external_id}, "
            f"SUP?: {self.supervisor})"
            f"Hours: {self.hours}, "
            f"Shift count: {self.shift_count}, "
        )

    def add_shift(self, day_id, shift_start, shift_end, hours, shift_group, station_name):
        self.schedule.append(Shift(day_id, shift_start, shift_end, hours, station_name, shift_group))
