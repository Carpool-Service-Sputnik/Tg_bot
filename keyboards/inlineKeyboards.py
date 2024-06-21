from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import math
from datetime import datetime
import calendar
from pytz import timezone


supportkb=InlineKeyboardMarkup(row_width=1)
url_tg=InlineKeyboardButton('@baze1evs',url='https://t.me/Baze1evs')
supportkb.add(url_tg)

becomekb=InlineKeyboardMarkup(row_width=1)
url_form_driver=InlineKeyboardButton("Форма",url='https://www.youtube.com/watch?v=HIcSWuKMwOw')
becomekb.add(url_form_driver)


def GenerationOfInlineButtons(data, title, rows=3, columns=6, page_number=0):
    """
    Generates a keyboard with inline buttons for use in Telegram Inline mode.

    Parameters:
    - data: list of data for the buttons.
    - title: the title of the keyboard.
    - rows: number of rows of buttons in the keyboard. Default is 3.
    - columns: number of columns of buttons in the keyboard. Default is 6.
    - page_number: the page number of the keyboard to display. Default is 0.

    Returns:
    Returns a list containing an InlineKeyboardMarkup object and the current page number.

    If the page number is out of range or equal to the number of pages, the function returns -2.

    Example usage:
    buttons = GenerationOfInlineButtons(data=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], title="Example Keyboard")
    keyboard = buttons[0]
    page_number = buttons[1]
    """

    prev_button = InlineKeyboardButton("◀️", callback_data="prev")
    next_button = InlineKeyboardButton("▶️", callback_data="next")
    cancel_button = InlineKeyboardButton("Отмена", callback_data="cancel")
    title_button = InlineKeyboardButton(f"{title}", callback_data="title")
    empty_button1 = InlineKeyboardButton("", callback_data="empty_button1")
    empty_button2 = InlineKeyboardButton("", callback_data="empty_button2")
    empty_button3 = InlineKeyboardButton("", callback_data="empty_button3")

    keyboards = InlineKeyboardMarkup(row_width=3)

    lenData = len(data)
    numberOfCells = rows * columns
    numberOfPages = math.ceil(lenData / numberOfCells)
    numberFirstElement = numberOfCells*page_number

    if page_number == numberOfPages or page_number < 0:
        return -2
    keyboards.add(title_button)
    keyboards.row(empty_button1, empty_button2, empty_button3)

    for i in range(numberFirstElement, numberFirstElement + numberOfCells):
        if i >= lenData:
            break
        button = InlineKeyboardButton(text=f"{data[i]}", callback_data=f"{data[i]}")
        keyboards.insert(button)
    keyboards.row(prev_button, cancel_button, next_button)

    return [keyboards, page_number]




class Colors:
    """
    A class representing a collection of colors with corresponding smiley icons as a Telegram inline keyboard.

    Attributes:
    - colors_smile: a dictionary mapping color names with their corresponding smiley icons.
    - buttons: a list of inline keyboard buttons generated from the colors_smile dictionary.
    - title_button: an inline keyboard button for the title of the keyboard.
    - empty_button1, empty_button2, empty_button3: empty inline keyboard buttons for layout purposes.
    - inline_keyboard_colors: an InlineKeyboardMarkup object containing the generated keyboard.

    Example usage:
    my_colors = Colors()
    keyboard = my_colors.inline_keyboard_colors
    """

    def __init__(self):
        self.colors_smile = {
            "Красный 🔴": "Красный",
            "Оранжевый 🟠": "Оранжевый",
            "Жёлтый 🟡": "Жёлтый",
            "Зеленый 🟢": "Зеленый",
            "Голубой 🌊": "Голубой",
            "Синий 🔵": "Синий",
            "Фиолетовый 💜": "Фиолетовый",
            "Розовый 🌸": "Розовый",
            "Коричневый 🟤": "Коричневый",
            "Серый 🌫️": "Серый",
            "Белый ⚪️": "Белый",
            "Чёрный ⚫️": "Черный"
        }

        self.empty_button1 = InlineKeyboardButton("", callback_data="empty_button1")
        self.empty_button2 = InlineKeyboardButton("", callback_data="empty_button2")
        self.empty_button3 = InlineKeyboardButton("", callback_data="empty_button3")

        self.buttons = [
            InlineKeyboardButton(text=color, callback_data=self.colors_smile[color]) for color in self.colors_smile
        ]

        self.title_button = InlineKeyboardButton("Цвета", callback_data="title")
        self.inline_keyboard_colors = InlineKeyboardMarkup(row_width=3).add(self.title_button)
        self.inline_keyboard_colors.row(self.empty_button1, self.empty_button2, self.empty_button3)
        self.inline_keyboard_colors.add(*self.buttons)




def GenerationOfInlineButtons_calendar(page_number=-2, year=-2, counter=0, limiter=True):

    moscow_tz = timezone('Europe/Moscow')
    current_date = datetime.now(moscow_tz)
    if year == -2:
            year = current_date.year
    if page_number == -2:
        page_number = current_date.month
    elif page_number < 1:
        page_number = 12
        year -= 1
    elif page_number > 12:
        page_number = 1
        year += 1

    result: list = [year, page_number]# упоковка ответа

    # Получение названия месяца на русском языке
    month_names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
    current_month = month_names[page_number - 1]
    if limiter == True:
        limiter = 11 - current_date.month
        if year == 2023:
            limiter += 12

    if counter > limiter + 1 or counter < 0:
        return -2




    days_in_month = {
        "Январь": range(1, 32),
        "Февраль": range(1, 30),
        "Март": range(1, 32),
        "Апрель": range(1, 31),
        "Май": range(1, 32),
        "Июнь": range(1, 31),
        "Июль": range(1, 32),
        "Август": range(1, 32),
        "Сентябрь": range(1, 31),
        "Октябрь": range(1, 32),
        "Ноябрь": range(1, 31),
        "Декабрь": range(1, 32)
    }


    last_day = calendar.monthrange(year, page_number)[1]

    # Определить день недели первого  и последнего дня месяца
    weekday_number = calendar.weekday(year, page_number, 1)
    weekday_of_last_day = calendar.weekday(year, page_number, last_day)

    title_button = InlineKeyboardButton(f"{current_month} {year}", callback_data="title")
    prev_button = InlineKeyboardButton("◀️", callback_data="prev")
    next_button = InlineKeyboardButton("▶️", callback_data="next")
    cancel_button = InlineKeyboardButton("Отмена", callback_data="cancel")
    empty_button1 = InlineKeyboardButton("", callback_data="empty_button1")
    empty_button2 = InlineKeyboardButton("", callback_data="empty_button2")
    empty_button3 = InlineKeyboardButton("", callback_data="empty_button3")
    week_monday = InlineKeyboardButton("Пон", callback_data="title")
    week_tuesday = InlineKeyboardButton("Вт", callback_data="title")
    week_wednesday = InlineKeyboardButton("Ср", callback_data="title")
    week_thursday = InlineKeyboardButton("Чт", callback_data="title")
    week_friday = InlineKeyboardButton("Пт", callback_data="title")
    week_saturday = InlineKeyboardButton("Сб", callback_data="title")
    week_sunday = InlineKeyboardButton("Вс", callback_data="title")


    keyboards = InlineKeyboardMarkup(row_width=7)

    keyboards.add(title_button)
    keyboards.row(empty_button1, empty_button2, empty_button3, empty_button1, empty_button2, empty_button3, empty_button1)

    keyboards.row(week_monday, week_tuesday, week_wednesday, week_thursday, week_friday, week_saturday, week_sunday)
    # keyboards.row(empty_button1, empty_button2, empty_button3, empty_button1, empty_button2, empty_button3, empty_button1)

    while weekday_number != 0:
        weekday_number -= 1
        button = InlineKeyboardButton(text=" ", callback_data="title")
        keyboards.insert(button)


    for i in days_in_month[current_month]:
        if i >= len(days_in_month[current_month]) + 1:
            break
        a = i
        b = page_number
        if i < 10: a = f"0{i}"
        if int(page_number) < 10: b = f"0{page_number}"
        button = InlineKeyboardButton(text=f"{i}", callback_data=f"{a}.{b}.{year}")
        keyboards.insert(button)


    while weekday_of_last_day != 6:
        weekday_of_last_day += 1
        button = InlineKeyboardButton(text=" ", callback_data="title")
        keyboards.insert(button)
    keyboards.row(prev_button, cancel_button, next_button)
    result.extend((keyboards, counter, limiter))

    return result





def GenerationOfInlineButtons_time(typeOfTime:str="hours", time_hours:str="0"):
    cancel_button = InlineKeyboardButton("Отмена", callback_data="cancel")
    empty_button1 = InlineKeyboardButton("", callback_data="empty_button1")
    keyboards = InlineKeyboardMarkup(row_width=4)


    if typeOfTime == "hours":
        _extracted_from_GenerationOfInlineButtons_time_(
            "Часы", keyboards, empty_button1
        )
        hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

        for i in hours:
            if i >= len(hours):
                break
            button = InlineKeyboardButton(text=f"{i}", callback_data=f"{i}")
            keyboards.insert(button)

    elif typeOfTime == "minutes":
        _extracted_from_GenerationOfInlineButtons_time_(
            "Минуты", keyboards, empty_button1
        )
        minutes = ["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"]

        for i in minutes:
            # if int(i) >= len(minutes):
            #     break
            button = InlineKeyboardButton(text=f"{time_hours}:{i}", callback_data=f"{time_hours}:{i}")
            keyboards.insert(button)

    keyboards.row(empty_button1, empty_button1)
    keyboards.row(cancel_button)

    return keyboards


# TODO Rename this here and in `GenerationOfInlineButtons_time`
def _extracted_from_GenerationOfInlineButtons_time_(arg0, keyboards, empty_button1):
    title_button = InlineKeyboardButton(arg0, callback_data="title")
    keyboards.add(title_button)
    keyboards.row(empty_button1, empty_button1)










