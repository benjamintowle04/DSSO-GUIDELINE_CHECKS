from models.guideline import Guideline
from models.requirement import Requirement
from models.dayRequirement import DayRequirement
from models.timeRequirement import TimeRequirement
from models.shiftTypeRequirement import ShiftTypeRequirement
from models.exceptions import Exceptions
from utils.checkboxDecoders import decodeDaysCheckboxCell, decodeShiftTypeCheckboxCell, decodeExceptionsCheckBoxCell
from utils.helperFunctions import column_index_from_string



def getFacilityGuidelineRegular(ws_reqs, ws_times):
    req_list = []
    excused_req_list = []
    shift_excused = None
    exceptions = None

    for row in ws_reqs.iter_rows(min_row=2):
        # Initialize column values from sheet
        row_number = row[0].row
        req_name = row[column_index_from_string("A") - 1].value
        req_type = row[column_index_from_string("B") - 1].value
        days = decodeDaysCheckboxCell(row_number, ws_reqs)
        min_start = row[column_index_from_string("D") - 1].value
        max_start = row[column_index_from_string("E") - 1].value
        min_end = row[column_index_from_string("F") - 1].value
        max_end = row[column_index_from_string("G") - 1].value
        cell_value = row[column_index_from_string("J") - 1].value
        min_exception_shifts = row[column_index_from_string("L") - 1].value
        exception_note = row[column_index_from_string("M") - 1].value
        shift_types_list = decodeShiftTypeCheckboxCell(row_number, ws_reqs)

        if not req_name or req_type == "None":
            continue

        if cell_value and cell_value.lower() == "y":
            excused = True
        else:
            excused = False

        if req_type == "Day":
            day_req_type = DayRequirement(days)
            day_req = Requirement(req_name, day_req_type, excused, None, 1)
            if excused and min_exception_shifts >= 1:
                excused_req_list = decodeExceptionsCheckBoxCell(
                    row_number, ws_reqs, ws_times
                )
                shift_excused = day_req
                exceptions = Exceptions(
                    exception_note,
                    excused_req_list,
                    shift_excused,
                    min_exception_shifts,
                )

                day_req.exception = exceptions

            req_list.append(day_req)

        elif req_type == "Time":
            time_req_type = TimeRequirement(min_start, max_start, min_end, max_end)
            time_req = Requirement(req_name, time_req_type, excused, None, 1)

            if excused and min_exception_shifts >= 1:
                excused_req_list = decodeExceptionsCheckBoxCell(
                    row_number, ws_reqs, ws_times
                )
                shift_excused = time_req
                exceptions = Exceptions(
                    exception_note,
                    excused_req_list,
                    shift_excused,
                    min_exception_shifts,
                )

                time_req.exception = exceptions

            req_list.append(time_req)

        elif req_type == "Shift Type":
            shiftType_req_type = ShiftTypeRequirement(shift_types_list)
            shiftType_req = Requirement(req_name, shiftType_req_type, excused, None, 1)
            if excused and min_exception_shifts >= 1:
                excused_req_list = decodeExceptionsCheckBoxCell(
                    row_number, ws_reqs, ws_times
                )
                shift_excused = shiftType_req
                exceptions = Exceptions(
                    exception_note,
                    excused_req_list,
                    shift_excused,
                    min_exception_shifts,
                )

                shiftType_req.exception = exceptions

            req_list.append(shiftType_req)

        else:
            print("Error: Invalid Input")

    return Guideline(req_list, exceptions, 8)


def getFacilityGuidelineSupervisor(ws_reqs, ws_times):
    req_list = []
    excused_req_list = []
    shift_excused = None
    exceptions = None

    for row in ws_reqs.iter_rows(min_row=2):
        # Initialize column values from sheet
        row_number = row[0].row
        req_name = row[column_index_from_string("A") - 1].value
        req_type = row[column_index_from_string("B") - 1].value
        days = decodeDaysCheckboxCell(row_number, ws_reqs)
        min_start = row[column_index_from_string("D") - 1].value
        max_start = row[column_index_from_string("E") - 1].value
        min_end = row[column_index_from_string("F") - 1].value
        max_end = row[column_index_from_string("G") - 1].value
        cell_value = row[column_index_from_string("J") - 1].value
        min_exception_shifts = row[column_index_from_string("L") - 1].value
        exception_note = row[column_index_from_string("M") - 1].value
        shift_types_list = decodeShiftTypeCheckboxCell(row_number, ws_reqs)

        if not req_name:
            continue

        if cell_value.lower() == "y":
            excused = True
        else:
            excused = False

        if req_type == "All SUP":
            shiftType_req_type = ShiftTypeRequirement(["All SUP"])
            shiftType_req = Requirement(req_name, shiftType_req_type, excused, None, 1)
            if excused and min_exception_shifts >= 1:
                excused_req_list = decodeExceptionsCheckBoxCell(
                    row_number, ws_reqs, ws_times
                )
                shift_excused = shiftType_req
                exceptions = Exceptions(
                    exception_note,
                    excused_req_list,
                    shift_excused,
                    min_exception_shifts,
                )

                shiftType_req.exception = exceptions

            req_list.append(shiftType_req)

        elif req_type == "One SUP":
            shiftType_req_type = ShiftTypeRequirement(["One SUP"])
            shiftType_req = Requirement(req_name, shiftType_req_type, excused, None, 1)
            if excused and min_exception_shifts >= 1:
                excused_req_list = decodeExceptionsCheckBoxCell(
                    row_number, ws_reqs, ws_times
                )
                shift_excused = shiftType_req
                exceptions = Exceptions(
                    exception_note,
                    excused_req_list,
                    shift_excused,
                    min_exception_shifts,
                )

                shiftType_req.exception = exceptions

            req_list.append(shiftType_req)

        elif req_type == "Multiple SUPs":
            shiftType_req_type = ShiftTypeRequirement(["Multiple SUPs"])
            shiftType_req = Requirement(req_name, shiftType_req_type, excused, None, 1)
            if excused and min_exception_shifts >= 1:
                excused_req_list = decodeExceptionsCheckBoxCell(
                    row_number, ws_reqs, ws_times
                )
                shift_excused = shiftType_req
                exceptions = Exceptions(
                    exception_note,
                    excused_req_list,
                    shift_excused,
                    min_exception_shifts,
                )

                shiftType_req.exception = exceptions

            req_list.append(shiftType_req)

        elif req_type == "Day":
            day_req_type = DayRequirement(days)
            day_req = Requirement(req_name, day_req_type, excused, None, 1)
            if excused and min_exception_shifts >= 1:
                excused_req_list = decodeExceptionsCheckBoxCell(
                    row_number, ws_reqs, ws_times
                )
                shift_excused = day_req
                exceptions = Exceptions(
                    exception_note,
                    excused_req_list,
                    shift_excused,
                    min_exception_shifts,
                )

                day_req.exception = exceptions

            req_list.append(day_req)

        elif req_type == "Time":
            time_req_type = TimeRequirement(min_start, max_start, min_end, max_end)
            time_req = Requirement(req_name, time_req_type, excused, None, 1)

            if excused and min_exception_shifts >= 1:
                excused_req_list = decodeExceptionsCheckBoxCell(
                    row_number, ws_reqs, ws_times
                )
                shift_excused = time_req
                exceptions = Exceptions(
                    exception_note,
                    excused_req_list,
                    shift_excused,
                    min_exception_shifts,
                )

                time_req.exception = exceptions

            req_list.append(time_req)

        elif req_type == "Shift Type":
            shiftType_req_type = ShiftTypeRequirement(shift_types_list)
            shiftType_req = Requirement(req_name, shiftType_req_type, excused, None, 1)
            if excused and min_exception_shifts >= 1:
                excused_req_list = decodeExceptionsCheckBoxCell(
                    row_number, ws_reqs, ws_times
                )
                shift_excused = shiftType_req
                exceptions = Exceptions(
                    exception_note,
                    excused_req_list,
                    shift_excused,
                    min_exception_shifts,
                )

                shiftType_req.exception = exceptions

            req_list.append(shiftType_req)

        else:
            print("Error: Invalid Input")

    return Guideline(req_list, exceptions, 13)



