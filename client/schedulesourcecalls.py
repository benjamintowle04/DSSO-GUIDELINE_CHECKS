import requests
import json
from urllib.parse import urlencode
from utils.paths import Paths
from client.credentials import load_creds
from utils.helperFunctions import isTSV, convertToJson


def authenticate():
    try:
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

        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        response_json = response.json()

        api_token = response_json["Response"]["APIToken"]
        session_id = response_json["Response"]["SessionId"]
        print("API TOKEN: ", api_token)
        print("SESSION ID", session_id)
        return {"sessionId": session_id, "apiToken": api_token}

    except requests.exceptions.RequestException as e:
        print(f"Error during authentication: {e}")
        return None
    except KeyError as e:
        print(f"Missing key in authentication response: {e}")
        return None


def getLocations():
    try:
        credentials = authenticate()
        if not credentials:
            return []

        base_url = "https://tmwork.net"
        url = f"{base_url}{Paths.SS_LOCATIONS.value}?Fields=Name"
        headers = {
            "Content-Type": "application/json",
            "x-session-id": credentials["sessionId"],
            "x-api-token": credentials["apiToken"],
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        filtered_data = [
            item["Name"]
            for item in data
            if item["Name"] in {"UDM", "Conversations", "Seasons", "Friley"}
        ]

        print(filtered_data)
        return filtered_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching locations: {e}")
        return []
    except KeyError as e:
        print(f"Missing key in locations data: {e}")
        return []


def getScheduleNames(location):
    try:
        credentials = authenticate()
        if not credentials:
            return {"Names": [], "ScheduleIds": []}

        url = "https://tmwork.net"
        path = Paths.SS_SCHEDULES.value
        query_params = {
            "Fields": "Name, ScheduleId",
            "MinDate": "2023-08-10",
            "MaxDate": "2030-05-10",
            "BusinessExternalId": location,
        }

        encoded_query_params = urlencode(query_params)
        full_url = f"{url}{path}?{encoded_query_params}"

        headers = {
            "Content-Type": "application/json",
            "x-session-id": credentials["sessionId"],
            "x-api-token": credentials["apiToken"],
        }

        response = requests.get(full_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        names = [item["Name"] for item in data]
        scheduleIds = [item["ScheduleId"] for item in data]

        print(names)
        print(scheduleIds)

        return {"Names": names, "ScheduleIds": scheduleIds}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching schedule names: {e}")
        return {"Names": [], "ScheduleIds": []}
    except KeyError as e:
        print(f"Missing key in schedule names data: {e}")
        return {"Names": [], "ScheduleIds": []}


def getAssignedShifts(location, scheduleId, start_date, end_date):
    try:
        credentials = authenticate()
        if not credentials:
            return []

        url = "https://tmwork.net"
        path = Paths.SS_SCHEDULE_SHIFTS.value
        query_params = {
            "Fields": "DayId,FirstName,LastName,EmployeeExternalId,ShiftStart,ShiftEnd,Hours,StationName,ShiftGroup",
            "MinDate": start_date.strftime("%Y-%m-%d"),
            "MaxDate": end_date.strftime("%Y-%m-%d"),
            "BusinessExternalId": location,
            "ScheduleId": scheduleId,
            "EmployeeExternalId": "{NOT NULL}",
        }

        encoded_query_params = urlencode(query_params)
        full_url = f"{url}{path}?{encoded_query_params}"

        headers = {
            "Content-Type": "application/json",
            "x-session-id": credentials["sessionId"],
            "x-api-token": credentials["apiToken"],
        }

        response = requests.get(full_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        filtered_shifts = [
            item for item in data if item.get("EmployeeExternalId") != "REMOVED"
        ]

        print(filtered_shifts)
        return filtered_shifts

    except requests.exceptions.RequestException as e:
        print(f"Error fetching assigned shifts: {e}")
        return []
    except KeyError as e:
        print(f"Missing key in assigned shifts data: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error in getAssignedShifts: {e}")
        return []


