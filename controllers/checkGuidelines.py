from models.employeeList import EmployeeList
from models.dayRequirement import DayRequirement
from models.timeRequirement import TimeRequirement
from models.shiftTypeRequirement import ShiftTypeRequirement
from utils.helperFunctions import convert_to_time
from controllers.initEmployees import initializeEmployees
from controllers.initGuidelines import getFacilityGuidelineRegular, getFacilityGuidelineSupervisor
from openpyxl import load_workbook
import os
import sys


#Need this function for pyinstaller to recognize the dependency
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = sys._MEIPASS
    else:
        # Running in a normal Python environment
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


#Algorithm for populating a list of employees that do not meet guidelines
#Returns a list of employees that have assigned shifts
#Initializes the "schedule_valid" field for each employee after checking if they meet requiremnets
#Inputs - guideline - schedule requirements for regular student workers
#         sup_guideline - schedule requirements for supervisors
#         employeeList  - list of all employees who have self-scheduled
def guidelineCheck(guideline, sup_guideline, employeeList):
    for employee in employeeList:
        if employee.supervisor == "Yes":
            req_list = sup_guideline.requirement_list
            if sup_guideline.exceptions:
                exceptions = sup_guideline.exceptions
                req_excused = exceptions.requirement_excused
            else:
                exceptions = None
            min_hours = sup_guideline.min_hours

        else:
            req_list = guideline.requirement_list
            exceptions = guideline.exceptions
            if exceptions:
                req_excused = exceptions.requirement_excused
            min_hours = guideline.min_hours

        employee.schedule_valid = True  # Employees are innocent until proven guilty
        for req in req_list:
            req_type = req.requirement_type
            req_name = req.requirement_name
            if not (
                    meetsRequirement(
                        employee, req_name, req_type, req.min_shifts, min_hours
                    )
            ):
                # Check for excuses in the requirement
                if req.exception and req == req_excused:
                    if excuseRequirement(employee, req.exception, req):
                        employee.notes = exceptions.exception_note

                        if req.requirement_name in employee.missing_reqs:
                            employee.missing_reqs.replace(req.requirement_name, "")

                    else:
                        employee.schedule_valid = False

                else:
                    employee.schedule_valid = False
    return employeeList



#Determines whether or not the requirement passed in should be excused based on facility guidelines
# if the minimum # of shifts needed to excuse the requirements are there, the app disregards this requirement
def excuseRequirement(employee, exceptions, req):
    req_list = (
        exceptions.excuse_req_list
    )  # If any of these requirements are met, it counts towards 1 shift in the min_shifts
    meets_req_count = 0
    min_shifts = exceptions.min_shifts

    for req in req_list:
        meets_req_count += countMetRequirements(employee, req.requirement_type)

    if meets_req_count >= min_shifts:
        return True

    else:
        return False

#Used for scheduling exceptions when an employee needs to work a minimum # of shifts
#Ex - 3+ breakfast/lunch shifts need to have a counter function to verify that at least 3 of these shifts are on the schedule
def countMetRequirements(employee, requirement_type):
    shift_count = 0

    #Case 1 : Requiremnet refers to what days are worked (ex - Weekend = Saturday & Sunday)
    if isinstance(requirement_type, DayRequirement):
        days = requirement_type.days_list
        for shift in employee.schedule:
            for day in days:
                if shift.day == day:
                    shift_count += 1

    #Case 2 - Requirement is a shift type requirement (ex dish, dining, BOH, etc)
    elif isinstance(requirement_type, ShiftTypeRequirement):
        types = requirement_type.types_list
        for shift in employee.schedule:
            for shiftType in types:
                if shift.station == shiftType:
                    shift_count += 1


    #Case 3 - Requirement is a time requirement
    elif isinstance(requirement_type, TimeRequirement):

        #Define the valid time ranges for the requirement
        min_start = requirement_type.min_start
        min_end = requirement_type.min_end
        max_start = requirement_type.max_start
        max_end = requirement_type.max_end

        # Set necessary upper/lower bounds of times for values that are null
        if min_start is None:
            min_start = convert_to_time("12:00:00 AM")

        if max_start is None:
            max_start = convert_to_time("11:59:00 PM")

        if min_end is None:
            min_end = convert_to_time("12:00:00 AM")

        if max_end is None:
            max_end = convert_to_time("11:59:00 PM")

        # Sift through schedule and make sure at least 1 shift is in range
        for shift in employee.schedule:

            # If a shift ends later than 12 AM, we want its end time to be at max
            if convert_to_time("12:00:00 AM") <= shift.end_time <= convert_to_time("3:00:00 AM"):
                shift.end_time = convert_to_time("11:59:00 PM")

            if min_start <= shift.start_time <= max_start and min_end <= shift.end_time <= max_end:
                shift_count += 1

    return shift_count


#Algorithm for determining if a requirement is met by the employee's schedule
#Returns true if it is met, false otherwise
def meetsRequirement(employee, requirement_name, requirement_type, min_shifts, min_hours):
    shift_count = 0
    meetsRequirement = False

    #Case 1
    if isinstance(requirement_type, DayRequirement):
        days = requirement_type.days_list
        for shift in employee.schedule:
            for day in days:
                if shift.day == day:
                    shift_count += 1
                    if shift_count == min_shifts:
                        meetsRequirement = True
        if not (meetsRequirement):
            employee.missing_reqs = employee.missing_reqs + " " + requirement_name

    #Case 2
    elif isinstance(requirement_type, ShiftTypeRequirement):
        types = requirement_type.types_list
        if "All SUP" in types:
            types = ["Supervisor"]
            min_shifts = employee.shift_count

        elif "One SUP" in types:
            types = ["Supervisor"]
            min_shifts = 1

        elif "Multiple SUPs" in types:
            types = ["Supervisor"]
            min_shifts = 2

        for shift in employee.schedule:
            for shiftType in types:
                if employee.supervisor == "Yes" and shiftType != "Supervisor":
                    m_shifts = 1
                    if shift.group == shiftType:
                        shift_count += 1
                        if shift_count == m_shifts:
                            meetsRequirement = True
                else:
                    if shift.station == shiftType:
                        shift_count += 1
                        if shift_count == min_shifts:
                            meetsRequirement = True
        if not (meetsRequirement):
            employee.missing_reqs = employee.missing_reqs + " " + requirement_name

    #Case 3
    elif isinstance(requirement_type, TimeRequirement):
        min_start = requirement_type.min_start
        min_end = requirement_type.min_end
        max_start = requirement_type.max_start
        max_end = requirement_type.max_end

        # Set necessary upper/lower bounds of times for values that are null
        if min_start == None or isinstance(min_start, str):
            min_start = convert_to_time("12:00:00 AM")

        if max_start == None or isinstance(max_start, str):
            max_start = convert_to_time("11:59:00 PM")

        if min_end == None or isinstance(min_end, str):
            min_end = convert_to_time("12:00:00 AM")

        if max_end == None or isinstance(max_end, str):
            max_end = convert_to_time("11:59:00 PM")

        # Sift through schedule and make sure at least 1 shift is in range
        for shift in employee.schedule:

            # If a shift ends later than 12 AM, we want its end time to be at max
            if shift.end_time >= convert_to_time("12:00:00 AM") and shift.end_time <= convert_to_time("3:00:00 AM"):
                shift.end_time = convert_to_time("11:59:00 PM")

            if (
                    min_start <= shift.start_time <= max_start
                    and min_end <= shift.end_time <= max_end
            ):
                shift_count += 1
                if shift_count == min_shifts:
                    meetsRequirement = True
        if not meetsRequirement:
            employee.missing_reqs = employee.missing_reqs + " " + requirement_name

    if employee.hours < min_hours:
        meetsRequirement = False
        if not ("Under Hours" in employee.missing_reqs):
            employee.missing_reqs = employee.missing_reqs + " Under Hours"

    return meetsRequirement


#Filter the list of employees after we check each one to see if they meet the guidelines (Ignoring SAMs)
#Each employee object has a schedule_valid field that dictates whether or not they should be on the callsheet
def filterList(employeeList):
    for employee in employeeList[:]:  # Iterate over a shallow copy of the list
        if employee.schedule_valid or "(SAM)" in employee.first_name:
            employeeList.remove(employee)

    return employeeList

#Set up the algorithms for checking guidelines
#Uses the external excel guideline files to initialize the appropriate objects
#
def runGuidelineCheck(location, scheduleId, start_date, end_date):
    employee_list = initializeEmployees(location, scheduleId, start_date, end_date)

    if location == "UDM":
        excel_file_name = "UDM_Guidelines.xlsx"
        ws_reqs_name_reg = "UDM Requirements"
        ws_reqs_name_sup = "UDM Supervisor Requirements"
        ws_times_name = "UDM Times in Need"

    elif location == "Seasons":
        excel_file_name = "Seasons_Guidelines.xlsx"
        ws_reqs_name_reg = "Seasons Requirements"
        ws_reqs_name_sup = "Seasons Supervisor Requirements"
        ws_times_name = "Seasons Times in Need"

    elif location == "Conversations":
        excel_file_name = "Conversations_Guidelines.xlsx"
        ws_reqs_name_reg = "Convos Requirements"
        ws_reqs_name_sup = "Convos Supervisor Requirements"
        ws_times_name = "Convos Times in Need"

    elif location == "Friley":
        excel_file_name = "Friley_Guidelines.xlsx"
        ws_reqs_name_reg = "Friley Requirements"
        ws_reqs_name_sup = "Friley Supervisor Requirements"
        ws_times_name = "Friley Times in Need"

    else:
        print("Error: Invalid Input")
        excel_file_name = ""
        ws_reqs_name_reg = ""
        ws_reqs_name_sup = ""
        ws_times_name = ""


    wb_path = resource_path(os.path.join("guideline_excel_sheets", excel_file_name))
    wb = load_workbook(wb_path)
    ws_reqs_reg = wb[ws_reqs_name_reg]
    ws_reqs_sup = wb[ws_reqs_name_sup]
    ws_times = wb[ws_times_name]

    guideline_regular = getFacilityGuidelineRegular(ws_reqs_reg, ws_times)
    guideline_supervisor = getFacilityGuidelineSupervisor(ws_reqs_sup, ws_times)
    employee_list = guidelineCheck(guideline_regular, guideline_supervisor, employee_list)


    employee_list = filterList(employee_list)


    return employee_list



