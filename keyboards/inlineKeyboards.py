from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import math
from datetime import datetime
import calendar
from pytz import timezone
from data.DirectionRoutesPoints import *
from func import *

supportkb = InlineKeyboardMarkup(row_width=1)
url_tg = InlineKeyboardButton('@baze1evs', url='https://t.me/Baze1evs')
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


class SimpleKeyboardsForReplenishBalance:
    confirm_button = InlineKeyboardButton(text='Подтвердить', callback_data='confirmation_of_replenishment_of_the_balance')
    cancel_button = InlineKeyboardButton(text='Отменить', callback_data='canceling_of_replenishment_of_the_balance')
    confirm_cancel_inline_kb = InlineKeyboardMarkup()
    confirm_cancel_inline_kb.insert(confirm_button).insert(cancel_button)

    # - - - top up with a certain amount
    top_up_amounts = [100.0, 200.0, 300.0, 500.0] # Если нужно добавить/изменить сумму, просто добавь в список нужное значение
    top_up_menu = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)

    for amount in top_up_amounts:
        button = InlineKeyboardButton(text=f"{amount} ₽", callback_data=f'top_up_rubles_{int(amount)}')
        top_up_menu.insert(button)


# - - - - - - - - - - - - -- - - - - - - --
def direction_keyboard():
    inline_kb = InlineKeyboardMarkup(row_width=2)
    direction1 = InlineKeyboardButton("Военвед - Центр", callback_data="voenC")
    direction2 = InlineKeyboardButton("Суворовский - Центр", callback_data="suvC")
    direction3 = InlineKeyboardButton("Северный - Центр", callback_data="sevC")
    direction4 = InlineKeyboardButton("Сельмаш - Центр", callback_data="selC")
    direction5 = InlineKeyboardButton("Западный - Центр", callback_data="zapC")
    direction6 = InlineKeyboardButton("Центр - Военвед", callback_data="cVoen")
    direction7 = InlineKeyboardButton("Центр - Суворовский", callback_data="cSuv")
    direction8 = InlineKeyboardButton("Центр - Северный", callback_data="cSev")
    direction9 = InlineKeyboardButton("Центр - Сельмаш", callback_data="cSel")
    direction10 = InlineKeyboardButton("Центр - Западный", callback_data="cZap")

    inline_kb.add(direction1, direction6, direction2, direction7, direction3, direction8, direction4,
                  direction9, direction5, direction10)

    return inline_kb


def route_keyboard(direction):
    inline_kb = InlineKeyboardMarkup(row_width=2)

    if (direction == "voenC"):
        route1 = InlineKeyboardButton('1', callback_data='voenCMarshrut1')
        route2 = InlineKeyboardButton('2', callback_data='voenCMarshrut2')
        inline_kb.add(route1, route2)
    if (direction == "suvC"):
        route1 = InlineKeyboardButton('1', callback_data='suvCMarshrut1')
        route2 = InlineKeyboardButton('2', callback_data='suvCMarshrut2')
        inline_kb.add(route1, route2)
    if (direction == "sevC"):
        route1 = InlineKeyboardButton('1', callback_data='sevCMarshrut1')
        route2 = InlineKeyboardButton('2', callback_data='sevCMarshrut2')
        inline_kb.add(route1, route2)
    if (direction == "selC"):
        route1 = InlineKeyboardButton('1', callback_data='selCMarshrut1')
        route2 = InlineKeyboardButton('2', callback_data='selCMarshrut2')
        route3 = InlineKeyboardButton('3', callback_data='selCMarshrut3')
        inline_kb.add(route1, route2, route3)
    if (direction == "zapC"):
        route1 = InlineKeyboardButton('1', callback_data='zapCMarshrut1')
        route2 = InlineKeyboardButton('2', callback_data='zapCMarshrut2')
        inline_kb.add(route1, route2)
    if (direction == "cVoen"):
        route1 = InlineKeyboardButton('1', callback_data='cVoenMarshrut1')
        route2 = InlineKeyboardButton('2', callback_data='cVoenMarshrut2')
        inline_kb.add(route1, route2)
    if (direction == "cSuv"):
        route1 = InlineKeyboardButton('1', callback_data='cSuvMarshrut1')
        route2 = InlineKeyboardButton('2', callback_data='cSuvMarshrut2')
        inline_kb.add(route1, route2)
    if (direction == "cSev"):
        route1 = InlineKeyboardButton('1', callback_data='cSevMarshrut1')
        route2 = InlineKeyboardButton('2', callback_data='cSevMarshrut2')
        inline_kb.add(route1, route2)
    if (direction == "cSel"):
        route1 = InlineKeyboardButton('1', callback_data='cSelMarshrut1')
        route2 = InlineKeyboardButton('2', callback_data='cSelMarshrut2')
        route3 = InlineKeyboardButton('3', callback_data='cSelMarshrut3')
        inline_kb.add(route1, route2, route3)
    if (direction == "cZap"):
        route1 = InlineKeyboardButton('1', callback_data='cZapMarshrut1')
        route2 = InlineKeyboardButton('2', callback_data='cZapMarshrut2')
        inline_kb.add(route1, route2)
    return inline_kb


def create_keyboard_for_choose_points(direction, route):
    route_number = extract_number(route)
    number_of_points = DirectionRoutesPoints.get_number_of_points_by_direction_and_route(direction, route_number)
    keyboard_list = []
    for i in range(number_of_points):
        point_text = DirectionRoutesPoints.get_point_by_direction_and_route(direction, route_number, i)
        button = InlineKeyboardButton(point_text, callback_data=i)
        keyboard_list.append(button)
    return keyboard_list

def all_dots_kb(route):
    direction_mapping = {
        'voenCMarshrut1': 'Военвед - Центр',
        'voenCMarshrut2': 'Военвед - Центр',
        'suvCMarshrut1': 'Суворовский - Центр',
        'suvCMarshrut2': 'Суворовский - Центр',
        'sevCMarshrut1': 'Северный - Центр',
        'sevCMarshrut2': 'Северный - Центр',
        'selCMarshrut1': 'Сельмаш - Центр',
        'selCMarshrut2': 'Сельмаш - Центр',
        'selCMarshrut3': 'Сельмаш - Центр',
        'zapCMarshrut1': 'Западный - Центр',
        'zapCMarshrut2': 'Западный - Центр',
        'cVoenMarshrut1': 'Центр - Военвед',
        'cVoenMarshrut2': 'Центр - Военвед',
        'cSuvMarshrut1': 'Центр - Суворовский',
        'cSuvMarshrut2': 'Центр - Суворовский',
        'cSevMarshrut1': 'Центр - Северный',
        'cSevMarshrut2': 'Центр - Северный',
        'cSelMarshrut1': 'Центр - Сельмаш',
        'cSelMarshrut2': 'Центр - Сельмаш',
        'cSelMarshrut3': 'Центр - Сельмаш',
        'cZapMarshrut1': 'Центр - Западный',
        'cZapMarshrut2': 'Центр - Западный'
    }

    direction = direction_mapping.get(route)
    if not direction:
        return None

    inline_kb = InlineKeyboardMarkup(row_width=1)
    for button in create_keyboard_for_choose_points(direction, route):
        inline_kb.add(button)

    return inline_kb


def point_A_keyboard(route):
    inline_kb = all_dots_kb(route=route)
    all_buttons = sum(inline_kb.inline_keyboard, [])[:-1]

    # Создаем новую клавиатуру и добавляем оставшиеся кнопки
    new_keyboard = InlineKeyboardMarkup(row_width=inline_kb.row_width)
    new_keyboard.inline_keyboard = [all_buttons[i:i + new_keyboard.row_width] for i in
                                    range(0, len(all_buttons), new_keyboard.row_width)]
    return new_keyboard


def point_B_keyboard(route, pointA):
    inline_kb = all_dots_kb(route=route)
    all_buttons = sum(inline_kb.inline_keyboard, [])

    # Удаляем первые n кнопок
    remaining_buttons = all_buttons[pointA:] if pointA <= len(all_buttons) else []

    # Создаем новую клавиатуру и добавляем оставшиеся кнопки
    new_keyboard = InlineKeyboardMarkup(row_width=inline_kb.row_width)
    new_keyboard.inline_keyboard = [remaining_buttons[i:i + new_keyboard.row_width] for i in
                                    range(0, len(remaining_buttons), new_keyboard.row_width)]
    return new_keyboard


def get_payment_keyboard():
    pay_button = InlineKeyboardButton(text="Оплатить", callback_data="pay")
    keyboard14 = InlineKeyboardMarkup().add(pay_button)
    return keyboard14