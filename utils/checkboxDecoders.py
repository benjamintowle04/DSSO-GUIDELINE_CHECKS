#Used to decode the checkboxes of the guideline excel files for each facility
#Pipes the data input by user into readable data for the program

from models.timeRequirement import TimeRequirement
from models.requirement import Requirement
from models.timeInNeed import TimeInNeed


def decodeShiftTypeCheckboxCell(row_number, ws):
    shift_list = []
    row_number *= 10
    dish = ws.cell(row=row_number, column=8).value
    dining = ws.cell(row=row_number + 1, column=8).value
    greeter = ws.cell(row=row_number + 2, column=8).value
    beverages = ws.cell(row=row_number + 3, column=8).value
    boh = ws.cell(row=row_number + 4, column=8).value
    na = ws.cell(row=row_number + 5, column=8).value

    if na:
        return []

    if dish:
        shift_list.append("Dish Room")
    if dining:
        shift_list.append("Dining Room")
    if greeter:
        shift_list.append("Greeter")
    if beverages:
        shift_list.append("Beverages")
    if boh:
        shift_list.append("Back of House")

    return shift_list


def decodeDaysCheckboxCell(row_number, ws):
    day_list = []
    row_number *= 10
    monday = ws.cell(row=row_number, column=3).value
    tuesday = ws.cell(row=row_number + 1, column=3).value
    wednesday = ws.cell(row=row_number + 2, column=3).value
    thursday = ws.cell(row=row_number + 3, column=3).value
    friday = ws.cell(row=row_number + 4, column=3).value
    saturday = ws.cell(row=row_number + 5, column=3).value
    sunday = ws.cell(row=row_number + 6, column=3).value
    na = ws.cell(row=row_number + 7, column=3).value

    if na:
        return []

    if monday:
        day_list.append("Monday")
    if tuesday:
        day_list.append("Tuesday")
    if wednesday:
        day_list.append("Wednesday")
    if thursday:
        day_list.append("Thursday")
    if friday:
        day_list.append("Friday")
    if saturday:
        day_list.append("Saturday")
    if sunday:
        day_list.append("Sunday")

    return day_list

def getTimesInNeed(ws):
    times_list = []

    if ws:
        for colA, colB, colC, colD, colE in zip(
            ws.iter_cols(min_col=1, max_col=1, min_row=2, values_only=True),
            ws.iter_cols(min_col=2, max_col=2, min_row=2, values_only=True),
            ws.iter_cols(min_col=3, max_col=3, min_row=2, values_only=True),
            ws.iter_cols(min_col=4, max_col=4, min_row=2, values_only=True),
            ws.iter_cols(min_col=5, max_col=5, min_row=2, values_only=True),
        ):
            for A, B, C, D, E in zip(colA, colB, colC, colD, colE):
                if A:
                    time_period = A
                    min_start = B
                    max_start = C
                    min_end = D
                    max_end = E
                    times_list.append(
                        TimeInNeed(time_period, min_start, max_start, min_end, max_end)
                    )

    return times_list


def decodeExceptionsCheckBoxCell(row_number, ws_reqs, ws_times):
    shift_list = []
    times_in_need = getTimesInNeed(ws_times)
    row_number *= 10
    breakfast = ws_reqs.cell(row=row_number, column=11).value
    lunch = ws_reqs.cell(row=row_number + 1, column=11).value
    dinner = ws_reqs.cell(row=row_number + 2, column=11).value
    late = ws_reqs.cell(row=row_number + 3, column=11).value
    na = ws_reqs.cell(row=row_number + 4, column=11).value

    if na:
        return []

    if breakfast:
        for item in times_in_need:
            if item.time_period == "Breakfast":
                req_type = TimeRequirement(
                    item.min_start, item.max_start, item.min_end, item.max_end
                )
                req = Requirement("Breakfast", req_type, False, None, 1)
                shift_list.append(req)

    if lunch:
        for item in times_in_need:
            if item.time_period == "Lunch":
                req_type = TimeRequirement(
                    item.min_start, item.max_start, item.min_end, item.max_end
                )
                req = Requirement("Lunch", req_type, False, None, 1)
                shift_list.append(req)

    if dinner:
        for item in times_in_need:
            if item.time_period == "Dinner":
                req_type = TimeRequirement(
                    item.min_start, item.max_start, item.min_end, item.max_end
                )
                req = Requirement("Dinner", req_type, False, None, 1)
                shift_list.append(req)

    if late:
        for item in times_in_need:
            if item.time_period == "Late":
                req_type = TimeRequirement(
                    item.min_start, item.max_start, item.min_end, item.max_end
                )
                req = Requirement("Late", req_type, False, None, 1)
                shift_list.append(req)

    return shift_list