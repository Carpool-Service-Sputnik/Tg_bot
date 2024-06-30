import string
import random
from datetime import datetime, timedelta
import os
import re




def split_text_into_words(txt):
    """Divide the text into words"""
    try:
        spl = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
        return txt.lower().translate(spl).split()
    except Exception as e:
        return []




def checking_string_in_list(path_file, txt):
    """Check the occurrence"""
    try:
        with open(f"{path_file}", "r") as file:
            content = file.read()
            counter = sum(i in content for i in txt if len(i) > 2)
        return [1] if counter > 0 else []
    except Exception as e:
        return []




def generateAlfNumStr(length, type_="all"):
    """Generate an alphanumeric, alphanumeric, or alphabetic random string"""
    if type_ == "all":
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.sample(letters_and_digits, length))
    elif type_ == "int":
        letters_and_digits = string.digits
        return ''.join(random.sample(letters_and_digits, length))
    elif type_ == "str":
        letters_and_digits = string.ascii_letters
        return ''.join(random.sample(letters_and_digits, length))
    else:
        return []




def algorithmForCalculatingSuitableTripsDate(jsonDate, userID, calculationError=0):
    """Calculation of a suitable trip by date for a specific user"""
    userData = jsonDate[userID]
    newJsonDate = jsonDate
    newJsonDate = {key: value for key, value in jsonDate.items() if key != f'{userID}'}
    date_user_dat = userData[0]
    try:date_user_dat_datetime = datetime.strptime(date_user_dat, "%d%m%Y")
    except:date_user_dat_datetime = datetime.strptime("12041961", "%d%m%Y")
    dictionaryWithMatchingIds = []
    for i in newJsonDate:
        date_users_dat = newJsonDate[f"{i}"][0]
        try:date_users_dat_datetime = datetime.strptime(date_users_dat, "%d%m%Y")
        except:date_users_dat_datetime = datetime.strptime("12041961", "%d%m%Y")
        difference = date_user_dat_datetime - date_users_dat_datetime
        if int(abs(difference.days)) <= calculationError:
            dictionaryWithMatchingIds.append(i)
    return dictionaryWithMatchingIds




def algorithmForCalculatingSuitableTripsTime(jsonDate, userID, SuitableIDs, calculationError=60):
    """Calculation of a suitable trip by time for a specific user"""
    userData = jsonDate[userID]
    newDict = {key: value for key, value in jsonDate.items() if key in SuitableIDs}
    time_user = userData[1]
    time_user_hours = int(time_user[:2])
    time_user_minutes = int(time_user[2:])
    timeUserMinutes = time_user_hours * 60 + time_user_minutes
    dictionaryWithMatchingIds = []
    for i in newDict:
        try:
            time_users = newDict[f"{i}"][1]
            time_users_hours = int(time_users[:2])
            time_users_minutes = int(time_users[2:])
        except Exception:pass
        else:
            timeUsersMinutes = time_users_hours * 60 + time_users_minutes
            if  abs(int(timeUserMinutes - timeUsersMinutes)) <= calculationError:
                dictionaryWithMatchingIds.append(i)
    return dictionaryWithMatchingIds




def remove_dicts_with_id(lst, vol, ke):
    """Creates a new list of dictionaries without a dictionary in which there is a match for one of the keys"""
    new_lst = [dict for dict in lst if dict.get(ke) != vol]
    return new_lst



def create_new_dict(ls):
    """Creates a new dictionary based on the dictionary list"""
    new_dict = {}
    for dct in ls:
        id_value = dct.get('id_trip')
        trips_dates_value = dct.get('tripsdates')
        trips_times_value = dct.get('tripstimes')
        if id_value:
            new_dict[id_value] = [trips_dates_value, trips_times_value]
    return new_dict




def filter_trip_list(trips_list, trip_point_a, trip_point_b):
    """Filters leaving only point A and point B"""
    filtered_trips = [
        trip
        for trip in trips_list
        if trip.get("pointa") == trip_point_a
        and trip.get("pointb") == trip_point_b
    ]
    return filtered_trips




def format_date_time(date_time: str):
    """Returns the date or time format"""
    if len(date_time) == 8:
        return f"{date_time[:2]}.{date_time[2:4]}.{date_time[4:]}"
    elif len(date_time) == 4:
        return f"{date_time[:2]}:{date_time[2:]}"
    else:
        return []




def generate_new_str(user_data):
    """Creates a row depending on the number of items in the list"""
    new_str = ""
    for i, data in enumerate(user_data):
        newStr = "Не актульная"
        if data["status"] == "agreed":
            newStr = "Согласованна"
        elif data["status"] == "waiting":
            newStr = "В ожидании"

        if data["typeofmembers"] == "driver":
            data["typeofmembers"] = "Водитель"
        elif data["typeofmembers"] == "passenger":
            data["typeofmembers"] = "Пассажир"

        new_str += f"""
{i + 1}.
Тип пользователя: {data["typeofmembers"]}
Дата поездки: {format_date_time(data["tripsdates"])}
Время поездки: {format_date_time(data["tripstimes"])}
От куда: {data["pointa"]}
Куда: {data["pointb"]}
Статус: {newStr}
"""
    return new_str


def generate_new_str_for_drivers(user_data):
    """Creates a row depending on the number of items in the list"""
    new_str = ""
    for i, data in enumerate(user_data):
        new_str += f"""
{i + 1}.
tg_id пользователя: {data["id_tg"]}
user_id пользователя: {data["id"]}
Имя: {data["name"]}
Фамилия: {data["surname"]}
Номер телефона: {data["numb"]}
"""
    return new_str



def get_next_error_number(path):
    """Reads the file and gives the error number"""
    try:
        if os.path.exists(path):
            with open(path, "r") as file:
                if lines := file.readlines():
                    last_line = lines[-1]
                    last_error_number = int(last_line.split(".")[0])
                    return last_error_number + 1
        return 1
    except Exception:
        return 1




def log_error(error_message):
    """Records errors"""
    try:
        timestamp = datetime.now().strftime("%d-%b-%Y %I:%M:%S %p")
        error_number = get_next_error_number("data//error_log.txt")
        with open("data/error_log.txt", "a") as file:
            file.write(f"{error_number}. {timestamp} - - - {error_message}\n")
    except Exception as e:
        error_message = str(e)
    else:
        timestamp = datetime.now().strftime("%d-%b-%Y %I:%M:%S %p")
        error_number = get_next_error_number("data//error_log.txt")
        with open("data/error_log.txt", "a") as file:
            file.write(f"{error_number}. {timestamp} - - - {error_message}\n")




def Accounting(tg_id):
    """Records the launch of the bot by users"""
    error_number = get_next_error_number("data//accounting.txt")
    now = datetime.now()
    with open('data//accounting.txt', 'a') as f:
        f.write(f'{error_number}. {now.date()} - - - {now.time()} - - - {tg_id}\n')



def remove_non_digits(text):
    """Removing all unnecessary characters"""
    if len(text) == 4:
        text = f"0{text}"
    newStr = re.sub(r'\D+', '', text)
    if len(newStr) == 6:
        year = str(datetime.now().year)[:2]
        newStr = f"{newStr[:4]}{year}{newStr[4:]}"
    elif len(newStr) == 2:
        while len(newStr) < 4:
            newStr += "0"
    elif len(newStr) == 3:
        newStr = f'{newStr[:2]}0{newStr[2:]}'
    elif len(newStr) not in {4, 8}:
        return []
    return newStr


def extract_number(string):
    match = re.search(r'\d+', string)
    return int(match.group()) if match else None


def foolproofCyrillic(text: str):
    """
    Foolproof cyrillic Function

    checks if all characters in the string are Cyrillic letters and returns True
    if so, and False if at least one character is not a Cyrillic letter, except
    for a space at the end of the text, except for a space at the end of the text

    :param text: String format text
    :type text: str
    :return: True or False
    :rtype: bool
    """
    cyrillic_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

    if text[-1] == " ":
        text = text.strip()

    return all(char.lower() in cyrillic_alphabet for char in text)


def foolproofPhoneNumber(text: str):
    """
    Foolproof Phone number Function

    checks if all characters in the string are digits and
    the "+" sign, and returns True if yes, and False if at
    least one character is not a digit or "+", except for a space at the end of the text

    :param text: String format text
    :type text: str
    :return: True or False
    :rtype: bool
    """
    Numb = '0123456789+'

    if text[-1] == " ":
        text = text.strip()

    return all(char.lower() in Numb for char in text)

def foolproofDate(date_str: str) -> bool:
    """
    Foolproof Date Function

    Verifies that a date string is in the correct format and no earlier than the current date.

    :param date_str: A string in format "dd.mm.yyyy" which needs to be checked.
    :type date_str: str
    :return: True if the date_str is in the correct format and no earlier than the current date,
    and False otherwise.
    :rtype: bool
    """
    try:
        date = datetime.strptime(date_str, '%d.%m.%Y')
        now = datetime.now()
        return date >= now
    except ValueError:
        return False


def calculate_trip_cost(start: int, end: int) -> int:
    """
    Calculate Trip Cost

    Calculates the cost of a trip based on the number of stops between the start and end points.

    :param start: The starting point of the trip (must be a non-negative integer).
    :type start: int
    :param end: The ending point of the trip (must be a non-negative integer and different from the starting point).
    :type end: int
    :return: The cost of the trip. Returns 0 if the start or end points are invalid or if they are the same.
    :rtype: int
    """
    if start < 0 or end < 0 or start == end:
        return 0
    
    stops = abs(end - start)
    
    if stops < 3:
        cost = 150
    elif 3 <= stops <= 5:
        cost = 200
    else:
        cost = 250
    
    return cost


def create_list_of_trips(tripsData: list, delay: int, status: int) -> list:
    """
    Create List of Trips

    Creates a filtered list of trips based on the provided trips data, current date and time, delay, and status.

    :param tripsData: A list of trip data, where each trip is represented as a dictionary.
    :type tripsData: list
    :param delay: The delay in minutes to be added to the trip time for comparison.
    :type delay: int
    :param status: The status filter for trips (0, 1, or 2).
                   0: Include trips that are not 'agreed' or 'waiting', or trips that have passed the adjusted trip time.
                   1: Include trips that are 'agreed' or 'waiting' and have not passed the adjusted trip time.
                   2: Include trips that fall within the delay period.
    :type status: int
    :return: A list of filtered trips based on the provided criteria.
    :rtype: list
    """
    current_datetime = datetime.now()
    data_list = []
    for data in tripsData:
        trip_status = data['status']
        trip_date = datetime.strptime(format_date_time(data['tripsdates']), "%d.%m.%Y").date()
        trip_time = (datetime.strptime(format_date_time(data['tripstimes']), "%H:%M")).time()
        trip_datetime = datetime.combine(trip_date, trip_time)

        if status == 0:
            trip_datetime = datetime.combine(trip_date, trip_time) + timedelta(minutes=delay)
            if not (trip_status == 'agreed' or trip_status == 'waiting'):
                data_list.append(data)
            elif current_datetime >= trip_datetime:
                data_list.append(data)

        elif status == 1:
            trip_datetime = datetime.combine(trip_date, trip_time) + timedelta(minutes=delay)
            if (trip_status in ['agreed', 'waiting']) and (current_datetime <= trip_datetime):
                data_list.append(data)

        elif status == 2:
            if (current_datetime >= trip_datetime) and (current_datetime <= trip_datetime + timedelta(minutes=delay)):
                data_list.append(data)

    return data_list



