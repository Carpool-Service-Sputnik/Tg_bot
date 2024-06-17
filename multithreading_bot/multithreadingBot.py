from func import *
from loader import BASE_URL
from loader import bt_token
import requests
from multithreading_bot import telegramAPI
from data import *


def passengerDateAndTimeCheck():
    try:
        dateRequest: dict
        dateRequest = requests.post(f"{BASE_URL}/gettrips/trips/suitableTrips", json="").json()
    except Exception as e:
        log_error(e)
        dateRequest = {"action":"technical maintenance"}

    if dateRequest != {"action":"technical maintenance"}:
        now_datetime = datetime.now()
        for i in dateRequest["data"]:
            tripsdate = datetime.strptime(f"{i['tripsdates']}", "%d%m%Y") 
            tripstime = datetime.strptime(f"{i['tripstimes']}", "%H%M")
            combined_datetime = datetime.combine(tripsdate.date(), tripstime.time())
            time_difference = combined_datetime - now_datetime 
            if time_difference.total_seconds() < 0:
                # Changing the status to inactive
                try:
                    dateRequest1: dict
                    dateRequest1 = requests.post(f"{BASE_URL}/updatetrips/trips/status", json={"status":"agreed", "id_trip":f"{i['id_trip']}"}).json()
                except Exception as e:
                    log_error(e)
                    dateRequest1 = {"action":"technical maintenance"}
                # if dateRequest != {"action":"technical maintenance"}:
            elif time_difference.total_seconds() > 0 and time_difference.total_seconds() / 60 < 30:
                try:
                    dateRequest_user: dict
                    dateRequest_user = requests.post(f"{BASE_URL}/getusers", json={"id":f'{i["id"]}'}).json()["data"]
                except Exception as e:
                    log_error(e)
                    dateRequest_user = {"action":f"technical maintenance {e}"}
                if dateRequest_user != {"action":"technical maintenance"}:
                    userData = remove_dicts_with_id(dateRequest["data"], i["id"], "id")
                    userDataPassengers_filter_trip_list = filter_trip_list(userData, i["pointa"], i["pointb"])
                    userData2 = create_new_dict(userDataPassengers_filter_trip_list)

                    userData2[i["id_trip"]] = [i["tripsdates"], i["tripstimes"]]
                    suitableTripIDs = algorithmForCalculatingSuitableTripsTime(userData2,  i["id_trip"], algorithmForCalculatingSuitableTripsDate(userData2, i["id_trip"]), 20)
                    
                    
                    if len(suitableTripIDs) > 0:
                        request_data = telegramAPI.send_message_keyboard(bt_token, dateRequest_user['id_tg'], text_3.t_taxi_ride, telegramAPI.inline_keyboards(suitableTripIDs))
                    
                    # # Changing the status to inactive
                    try:
                        dateRequest2: dict
                        dateRequest2 = requests.post(f"{BASE_URL}/updatetrips/trips/status", json={"status":"agreed", "id_trip":f"{i['id_trip']}"}).json()
                    except Exception as e:
                        log_error(e)
                        dateRequest2 = {"action":"technical maintenance"}

