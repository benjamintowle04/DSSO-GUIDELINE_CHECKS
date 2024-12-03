from datetime import datetime, time
import json


def binary_search_employee(data, target_id):
    left = 0
    right = len(data) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_id = int(data[mid]['EmployeeExternalId'])

        if mid_id == target_id:
            return data[mid]
        elif mid_id < target_id:
            left = mid + 1
        else:
            right = mid - 1

    return None


def convert_to_time(time_input):
    # Check if the input is a datetime object
    if isinstance(time_input, datetime):
        datetime_obj = time_input
    else:
        # Define the datetime formats
        date_only_format = "%Y-%m-%d"
        full_datetime_format = "%m/%d/%Y %I:%M:%S %p"
        time_only_format = "%I:%M:%S %p"
        iso_datetime_format = "%Y-%m-%dT%H:%M:%S"

        try:
            # Try to parse the full date-time string
            datetime_obj = datetime.strptime(time_input, full_datetime_format)
        except ValueError:
            try:
                # If that fails, try to parse the ISO date-time string
                datetime_obj = datetime.strptime(time_input, iso_datetime_format)
            except ValueError:
                try:
                    # If that fails, try to parse the time-only string
                    datetime_obj = datetime.strptime(time_input, time_only_format)
                except ValueError:
                    try:
                        datetime_obj = time(23, 59, 0)
                    except ValueError:
                        datetime_obj = None
                        print("Invalid Time Input")

    # Extract the time component from the datetime object
    if isinstance(datetime_obj, datetime):
        time_struct = datetime_obj.time()
        return time_struct


    else:
        return datetime_obj


def column_index_from_string(column):
    index = 0
    for char in column.upper():
        index = index * 26 + (ord(char) - ord("A") + 1)
    return index


def convert_dayId_to_day(dayId):
    if dayId == 1:
        return "Sunday"
    elif dayId == 2:
        return "Monday"
    elif dayId == 3:
        return "Tuesday"
    elif dayId == 4:
        return "Wednesday"
    elif dayId == 5:
        return "Thursday"
    elif dayId == 6:
        return "Friday"
    elif dayId == 7:
        return "Saturday"


#Retrieves the list of strings representing each facilities name
#Used to ensure that the list displayed in the app's dropdown menu are purely strings and not json objects
#Param - locations - list of json objects with an "ExternalBusinessIdField"
#Returns the list of strings each representing the value of the ExternalBusinessId field for each location
def getLocationNames(locations):
    string_list = []
    for item in locations:
        string_list.append(item)
    return string_list


# Check if data is in json format or TSV format
# Return true if data is in TSV format, false otherwise
def isTSV(response):
    try:
        # Step 1: Try to decode JSON. If this succeeds, return False.
        json.loads(response.decode('utf-8'))
        return False
    except (json.JSONDecodeError, UnicodeDecodeError):
        # If JSON decoding fails, check if the format is tab-delimited.
        try:
            decoded_response = response.decode('utf-8')
            # Step 2: Split by lines and tabs to check the format
            lines = decoded_response.split('\r\n')
            for line in lines:
                # If any line has more than 1 tab character, it's likely tab-delimited
                if len(line.split('\t')) > 1:
                    return True
            return False
        except UnicodeDecodeError:
            return False


import json


def convertToJson(response):
    try:
        # Try to decode JSON, if successful, return the already existing JSON
        return json.loads(response.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # If not JSON, proceed with tab-delimited parsing
        try:
            decoded_response = response.decode('utf-8')
            lines = decoded_response.split('\r\n')  # Split by lines

            # Initialize an empty list to store the parsed data
            data_list = []

            for line in lines:
                # Split each line by tab characters
                items = line.split('\t')
                # Filter out empty items caused by trailing tabs/newlines
                filtered_items = list(filter(None, items))
                if filtered_items:
                    data_list.append(filtered_items)

            # Convert to JSON-like structure (list of dictionaries)
            if data_list:
                # Assuming the first line contains column headers
                headers = data_list[0]
                records = data_list[1:]

                # Build list of dictionaries using headers as keys
                json_data = [dict(zip(headers, record)) for record in records]
                return json_data

            return {}  # Return an empty dict if no data was found
        except UnicodeDecodeError:
            return {}  # Return an empty dict if decoding fails


from datetime import datetime


def convert_to_12hr_format(time_str):
    """
    Converts a 24-hour formatted time string to 12-hour format with AM/PM.

    Args:
        time_str (str): Time in 24-hour format (e.g., "14:34:45").

    Returns:
        str: Time in 12-hour format with AM/PM (e.g., "02:34:45 PM").
    """
    # Parse the time string into a datetime object
    time_obj = datetime.strptime(time_str, "%H:%M:%S")

    # Format the time to 12-hour format with AM/PM
    return time_obj.strftime("%I:%M:%S %p")


# Example usage
formatted_time = "14:34:45"
converted_time = convert_to_12hr_format(formatted_time)
print("12-hour format:", converted_time)
