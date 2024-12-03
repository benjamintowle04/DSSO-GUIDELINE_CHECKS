class Requirement:
    def __init__(self, requirement_name, requirement_type, excused, exception, min_shifts):
        self.requirement_name = requirement_name
        self.requirement_type = requirement_type
        self.excused = excused
        self.exception = exception
        self.min_shifts = min_shifts
        