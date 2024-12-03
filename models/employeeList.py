from models.employee import Employee
from models.shift import Shift
from client.schedulesourcecalls import getAssignedShifts
from utils.helperFunctions import binary_search_employee, convert_to_time, convert_dayId_to_day


class EmployeeList:
    def __init__(self):
        self.employees = []

    #initializes employee objects with firstName, lastName, ID, and supervisor fields
    #All other fields set to default and are to be initialized elsewhere in the program
    # IMPORTANT!!! When using an employeeList object, make sure to initialize credentials first and then schedule
    def initEmployeeCredentials(self, total_shifts):
        if not self.employees:
            self.employees = []


        for shift in total_shifts:
            employee_ids = {employee.external_id for employee in self.employees}

            if shift['EmployeeExternalId'] in employee_ids:
                continue

            else:
                sup = "Yes" if "(SUP)" in shift["FirstName"] else "No"

                self.employees.append(Employee(shift["LastName"], shift["FirstName"], shift["EmployeeExternalId"],
                                               0, 0.0, sup, "", [],
                                               True, ""))


    # Gets the list of shifts that an employee with a specified id has assigned to them
    #Initializes the shifts, hours, and shiftCount for the employee
    def initEmployeeShiftData(self, total_shifts):
        for shift in total_shifts:
            if "Justice" in shift["LastName"]:
                print(shift)

        for employee in self.employees:
            employee_id = employee.external_id
            shift_to_append = binary_search_employee(total_shifts, int(employee_id))
            hours_count = 0.0

            # Set Employee Shifts
            while shift_to_append:
                shift_obj_to_append = Shift(convert_dayId_to_day(shift_to_append["DayId"]),
                                            convert_to_time(shift_to_append["ShiftStart"]),
                                            convert_to_time(shift_to_append["ShiftEnd"]),
                                            shift_to_append["Hours"],
                                            shift_to_append["StationName"],
                                            shift_to_append["ShiftGroup"])

                employee.schedule.append(shift_obj_to_append)
                total_shifts.remove(shift_to_append)
                hours_count += shift_to_append["Hours"]
                shift_to_append = binary_search_employee(total_shifts, int(employee_id))

            # Set Employee Shift Count
            employee.shift_count = len(employee.schedule)

            # Set Employee Hours
            employee.hours = hours_count







# # Testing Constructor
# obj = EmployeeList([])
# shifts = obj.getShiftsInSchedule("UDM", "398997")
#
# #Testing Credentials
# obj.initEmployeeCredentials(shifts)
# # for employee in obj.employees:
# #     print(employee.first_name + " " + employee.last_name)
#
#
# # Testing Shifts Append Function
# employee_to_test = obj.employees[59]
# obj.initEmployeeShifts(shifts)
# print(employee_to_test.first_name + " " + employee_to_test.last_name)
#
# for shift in employee_to_test.schedule:
#     print(shift.start_time + " " + shift.end_time + " " + shift.station)
#
# print(employee_to_test.shift_count)
# print(employee_to_test.hours)
# print("SUP? " + employee_to_test.supervisor)



