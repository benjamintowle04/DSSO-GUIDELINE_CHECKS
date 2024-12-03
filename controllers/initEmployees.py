from models import employeeList
from models.employeeList import EmployeeList
from client.schedulesourcecalls import getAssignedShifts

def getScheduleData(loation, scheduleId, start_date, end_date):
    ret = []
    try:
        ret = getAssignedShifts(loation, scheduleId, start_date, end_date)
    except Exception as e:
        print("ERROR OCCURED FETCHING SHIFT DATA" + e)

    if ret:
        ret.sort(key=lambda x: int(x['EmployeeExternalId']))
        return ret

    else:
        print("No Data Returned")
        return None


def initializeEmployees(location, scheduleId, start_date, end_date):
    total_employees = EmployeeList()
    total_shifts = getScheduleData(location, scheduleId, start_date, end_date)

    try:
        total_employees.initEmployeeCredentials(total_shifts)
        total_employees.initEmployeeShiftData(total_shifts)
    except Exception as e:
        print("Error Occurred: No data recieved from Schedule Source")
        return None

    return total_employees.employees






