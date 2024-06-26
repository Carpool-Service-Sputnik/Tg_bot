from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


# General section
class GeneralKeyboards():
    """
    Class with buttons for the bot.

    Attributes:
    - Buttons
    - Single keyboards
    - Group keyboards

    Example usage:
    my_keyboards = GeneralKeyboards()
    start_menu_keyboard = my_keyboards.group_startMenu

    reply_markup=GeneralKeyboards.mainMenu)
    """
    # Buttons
    btn_sign = KeyboardButton('Зарегистрироваться! 🐣')
    btn_about_service = KeyboardButton('О сервисе')
    btn_description = KeyboardButton('Описание')
    btn_rules = KeyboardButton('Правила сервиса')
    btn_questions = KeyboardButton('F.A.Q.')
    btn_next = KeyboardButton("Далее")
    btn_main_menu = KeyboardButton('Главное меню')
    btn_main = KeyboardButton('Вернуться в главное меню')
    btn_profile = KeyboardButton('Профиль')
    btn_my_trips = KeyboardButton('Мои поездки')
    btn_support = KeyboardButton('Поддержка')
    btn_create_trip = KeyboardButton('Создать поездку')
    btn_back = KeyboardButton('Вернунться назад')
    btn_command_start = KeyboardButton("/start")
    btn_command_menu = KeyboardButton("/menu")
    btn_status_P = KeyboardButton("Пассажир")
    btn_status_P_test = KeyboardButton("Пассажир_тест")
    btn_status_D = KeyboardButton("Водитель")
    btn_yes = KeyboardButton("Да")
    btn_no = KeyboardButton("Нет")
    btn_send_number = KeyboardButton(text="Отправить номер", request_contact=True)
    button_center = KeyboardButton("Центр")
    button_levencovka = KeyboardButton("Левенцовка")
    button_suvorovskiy = KeyboardButton("Суворовский")
    btn_top_up_balabce = KeyboardButton("Пополнить баланс")  # Profile menu button
    btn_check_balance = KeyboardButton("Текущий баланс")  # Profile menu button
    btn_check_current_trips = KeyboardButton("Текущие поездки") # Check trips menu button
    btn_check_past_trips = KeyboardButton("Прошлые поездки") # Check trips menu button

    # Single keyboards

    # - - - Next - - -
    single_btn_next = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    single_btn_next.add(btn_next)

    # - - - Main - - -
    single_btn_main = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    single_btn_main.add(btn_main)

    # - - - Command Start - - -
    single_btn_command_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    single_btn_command_start.add(btn_command_start)

    # - - - Profile buttons: About top up and check balance - - -
    group_profileMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    group_profileMenu.add(btn_check_balance, btn_top_up_balabce, btn_main)

    # - - - Command Start - - -
    single_btn_command_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    single_btn_command_menu.add(btn_command_menu)

    # - - - Send number - - -
    single_send_number = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    single_send_number.add(btn_send_number)

    # Group keyboards

    # - - - Start Menu - - -
    group_startMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn_sign)
    group_startMenu.row(btn_about_service)

    # - - - About service Menu not registered - - -
    group_aboutServiceMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn_description, btn_rules, btn_questions, btn_back)

    # - - - About service Menu - - -
    group_aboutServiceMenuRegistered = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_description, btn_rules).row(btn_questions, btn_main)

    # - - - Main Menu - - -
    mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_profile)
    mainMenu.row(btn_create_trip, btn_my_trips).row(btn_support, btn_about_service)

    # - - - Current or past trips
    group_check_trips_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    group_check_trips_menu.add(btn_check_current_trips, btn_check_past_trips).row(btn_main)

    # - - - Driver or passenger - - -
    group_status = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    group_status.add(btn_status_P, btn_status_D).row(btn_status_P_test)

    # - - - Yes or No - - -
    group_yesNo = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    group_yesNo.add(btn_yes, btn_no)

    # - - - Three popular points (districts) in the city of Rostov-on-Don - - -
    group_districts = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    group_districts.add(button_levencovka, button_suvorovskiy, button_center)


