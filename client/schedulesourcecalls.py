#File is dedicated to making the necessary api calls to retrieve a facility schedule
#Schedule is expected to be populated with employees and is used to perform automatic guideline checks
#Client Utilizes ScheduleSource's RESTful API to generate the call sheet to the user
#Author - Benjamin Towle
import requests
import json
import http
from urllib.parse import urlencode
from utils.paths import Paths
from client.credentials import load_creds
from utils.helperFunctions import isTSV, convertToJson


#Used to sign in to mgr portal of schedule source.
#Params: "code" - facility code used to sign in ("ISU For all")
#        "username" - mgr username used to sign in
#        "password" - mgr password used to sign in
#
#  Returns: API token and Session ID codes. Needed to be used as headers to retrieve information from API
def authenticate():
    creds = load_creds()
    url = "https://tmwork.net/api/ops/auth"

    payload = json.dumps(
        {
            "Request": {
                "Portal": "mgr",
                "Code": creds.code,
                "Username": "btowle04",
                "Password": "6269",
            }
        }
    )

    headers = {
        "Content-Type": "application/json",
        "BuildCookie": "24060420361420.32735534d2ac453faeb6fc50bf314f4d",
        "Cookie": "BuildCookie=24060420361420.32735534d2ac453faeb6fc50bf314f4d",
    }

    response = requests.request("POST", url, data=payload, headers=headers, )
    response_json = response.json()
    api_token = response_json["Response"]["APIToken"]
    session_id = response_json["Response"]["SessionId"]
    print("API TOKEN: ", api_token)
    print("SESSION ID", session_id)
    return {"sessionId": session_id, "apiToken": api_token}


# Direct API Call to retrieve a list of locations and their respective ID's
# Returns a list of the json data retrieved from the API call
# No Parameter values
# Returns list of json data that are valid location facility codes
def getLocations():
    credentials = authenticate()
    conn = http.client.HTTPSConnection("tmwork.net")
    payload = ""

    headers = {
        "Content-Type": "application/json",
        "x-session-id": credentials["sessionId"],
        "x-api-token": credentials["apiToken"],
    }

    base_url = Paths.SS_LOCATIONS.value
    url = (
        f"{base_url}"
        "?Fields=Name"
    )

    conn.request(
        "GET",
        url,
        payload,
        headers,
    )

    # Get response
    res = conn.getresponse()
    data = res.read()

    if isTSV(data):
        json_data = convertToJson(data)

    else:
        json_data = json.loads(data)


    # Filter out data that is null, or not a string
    filtered_data = []
    for item in json_data:
        if (item["Name"] == "UDM"
                or item["Name"] == "Conversations"
                or item["Name"] == "Seasons"
                or item["Name"] == "Friley"):
            filtered_data.append(item["Name"])


    print(filtered_data)
    return filtered_data


# API call to get the list of all schedules active in a specific date range (now to 6 years in the future)
# Param - location - the facility code selected in the first dropdown menu, used as query parameter in api call
# Returns a list of strings that represent the name of each schedule specific to "location"
def getScheduleNames(location):

    #TODO: Change this function so that it returns both the schedule Id and the name in a list
    credentials = authenticate()
    conn = http.client.HTTPSConnection("tmwork.net")
    payload = ""

    headers = {
        "Content-Type": "application/json",
        "x-session-id": credentials["sessionId"],
        "x-api-token": credentials["apiToken"],
    }

    path = Paths.SS_SCHEDULES.value
    query_params = {
        "Fields": "Name, ScheduleId",
        "MinDate": "2023-08-10",
        "MaxDate": "2030-05-10",
        "BusinessExternalId": location
    }

    encoded_query_params = urlencode(query_params)
    url = f"{path}?{encoded_query_params}"

    conn.request(
        "GET",
        url,
        payload,
        headers,
    )

    # Get response from backend SS server
    res = conn.getresponse()
    data = res.read()

    if isTSV(data):
        json_data = convertToJson(data)

    else:
        json_data = json.loads(data)


    # Populate a simple list of name strings to be used by applications dropdown menu
    names = []
    scheduleIds = []
    for item in json_data:
        names.append(item["Name"])
        scheduleIds.append(item["ScheduleId"])

    print(names)
    print(scheduleIds)

    return {
        "Names": names,
        "ScheduleIds": scheduleIds
        }



# # Get the specific schedule ID from the facility name and the name of the schedule.
# # ID will be used to get shift information of the schedule
# # Params: "facilityName" - the name of the facility we are pulling the schedule from (e.g "dsso", "udm", "friley", etc)
# #        "scheduleName" - the name of the schedule we want to pull shifts from (e.g "UDM Spring 2024 Master")
# #
# # Returns the schedule ID used to access the shift information of the specific schedule
# def getScheduleId(scheduleName):
#     credentials = authenticate()
#     conn = http.client.HTTPSConnection("tmowrk.net")
#     payload = ""
#
#     headers = {
#         "Content-Type": "application/json",
#         "x-session-id": credentials["sessionId"],
#         "x-api-token": credentials["apiToken"],
#     }
#
#     path = Paths.SS_SCHEDULES.value
#     query_params = {
#         "Fields": "ScheduleId",
#         "MinDate": "2023-08-10",
#         "MaxDate": "2030-05-10",
#         "Name": scheduleName
#     }
#
#     encoded_query_params = urlencode(query_params)
#     url = f"{path}?{encoded_query_params}"
#
#     conn.request(
#         "GET",
#         url,
#         payload,
#         headers,
#     )
#
#     res = conn.getresponse()
#     data = res.read()
#
#     try:
#         if isTSV(data):
#             json_data = convertToJson(data)
#
#         else:
#             json_data = json.loads(data)
#
#         json_object = json_data[0]
#         scheduleId = json_object.get("ScheduleId")
#         print("Schedule ID: " + str(scheduleId))
#         return scheduleId
#     except Exception as e:
#         print("An error has occurred while fetching Schedule ID: " + e)
#         return None


#Get a list of all active employees at a location
#Used to initialize employee names and supervisor status
def getAssignedShifts(location, scheduleId, start_date, end_date):
    credentials = authenticate()
    conn = http.client.HTTPSConnection("tmwork.net")
    payload = ""

    headers = {
        "Content-Type": "application/json",
        "x-session-id": credentials["sessionId"],
        "x-api-token": credentials["apiToken"],
    }

    path = Paths.SS_SCHEDULE_SHIFTS.value
    query_params = {
        "Fields": "DayId,FirstName,LastName,EmployeeExternalId,ShiftStart,ShiftEnd,Hours,StationName,ShiftGroup",
        "MinDate": start_date.strftime("%Y-%m-%d"),
        "MaxDate": end_date.strftime("%Y-%m-%d"),
        "BusinessExternalId": location,
        "ScheduleId": scheduleId,
        "EmployeeExternalId": "{NOT NULL}"
    }

    encoded_query_params = urlencode(query_params)
    url = f"{path}?{encoded_query_params}"

    conn.request(
        "GET",
        url,
        payload,
        headers,
    )

    try:
        res = conn.getresponse()
        data = res.read().decode('utf-8')
        json_data = json.loads(data)
        print(json_data)
        return [item for item in json_data if item['EmployeeExternalId'] != "REMOVED"]
    except Exception as e:
        print("An error has occurred while fetching Employee for Location: " + e)
        return None


