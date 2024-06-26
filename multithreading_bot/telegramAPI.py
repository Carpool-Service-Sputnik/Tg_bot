import requests
import json
from func import *







# _ _ _ Creating buttons _ _ _


# inline keyboards
def inline_keyboards(id_trip):


    inline_keyboard1 = {
        "inline_keyboard": [
            [
                {
                    "text": "Отлично",
                    "callback_data": f"{id_trip}"
                }
            ]
        ]
    }


    inline_keyboard2 = {
        "inline_keyboard": [
            [
                {
                    "text": "Отмена поездки",
                    "callback_data": "cancel a trip"
                }
            ]
        ]
    }

    # Combining both inline_keyboard objects
    inline_keyboard = {
        "inline_keyboard": [
            *inline_keyboard1["inline_keyboard"],
            *inline_keyboard2["inline_keyboard"]
        ]
    }


    # Converting a combined object with buttons to a JSON string
    reply_markup_inline = json.dumps(inline_keyboard)

    return reply_markup_inline



# _ _ _ Sending messages _ _ _


# Sending messages with the keyboard
def send_message_keyboard(bt_token, chat_id, text, reply_markup):
    try:
        # Generating a URL request with the combined reply_markup parameter
        url = f"https://api.telegram.org/bot{bt_token}/sendMessage?chat_id={chat_id}&text={text}&reply_markup={reply_markup}"

        # Sending a request
        response = requests.get(url)

        return response

    except Exception as e:
        log_error(e)

