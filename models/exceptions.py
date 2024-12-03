class Exceptions:
    def __init__(
        self, exception_note, excuse_req_list, requirement_excused, min_shifts
    ):
        self.exception_note = exception_note
        self.excuse_req_list = excuse_req_list
        self.requirement_excused = requirement_excused
        self.min_shifts = min_shifts