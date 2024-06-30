from datetime import datetime
from datetime import time
from datetime import timedelta
from aiogram import types
from aiogram.dispatcher import FSMContext
import keyboards.inlineKeyboards
from loader import ts
from loader import bot
from loader import dp
from loader import BASE_URL
from data import *
from states import *
from keyboards import *
import requests
from func import *
from data import DirectionRoutesPoints
import re

# _ _ _ Common commands _ _ _


async def aboutCommand(message: types.Message):
    """
    aboutCommand function

    Displays information about the service to the user who is not registered

    :param message: The message containing the user's input
    :type message: types.Message
    :send_message: Text containing the information about the service
    :type: Text
    """

    # Depending on the content of the message, it sends the appropriate information to the user
    if message.text == "F.A.Q.":
        await bot.send_message(message.from_user.id, text_2.t_FAQ, reply_markup=GeneralKeyboards.group_aboutServiceMenu)
    elif message.text == "Правила сервиса":
        await bot.send_message(message.from_user.id, text_2.t_rules, reply_markup=GeneralKeyboards.group_aboutServiceMenu)
    elif message.text == "Описание":
        await bot.send_message(message.from_user.id, text_2.t_about, reply_markup=GeneralKeyboards.group_aboutServiceMenu)
    elif message.text == "Вернунться назад":
        await UserState.start_register.set()
        await bot.send_message(message.from_user.id, text_1.t_time, reply_markup=GeneralKeyboards.group_startMenu)


async def startCommand(message: types.Message):
    """
    startCommand function

    Initializes user data and checks if the user is registered in the service

    :param message: The message containing the user's input
    :type message: types.Message
    :init_user_data: Initialize user data dictionaries
    :type: Data
    :register_user: Register user in the service
    :type: Function
    :check_user_registration: Check if the user is registered in the service
    :type: Function
    :send_message: Text containing welcome message or error message
    :type: Text
    """
    # Initialize global variables
    global dataAboutUser, dataAboutTrip, dataAboutCar
    # Initialize user data dictionaries
    dataAboutUser[message.from_user.id] = {"user_tg_id": message.from_user.id}
    dataAboutTrip[message.from_user.id] = {"user_tg_id": message.from_user.id}
    dataAboutCar[message.from_user.id] = {"user_tg_id": message.from_user.id}

    # Register user in the service
    Accounting(dataAboutUser[message.from_user.id]["user_tg_id"])

    # Check if the user is registered in the service
    try:
        dateRequest: dict
        dateRequest = requests.post(
            f"{BASE_URL}/checkuser", json={"id_tg": dataAboutUser[message.from_user.id]["user_tg_id"]}).json()
    except Exception as e:
        log_error(e)
        dateRequest = {"action": "technical maintenance"}
    if dateRequest["action"] == "success" and dateRequest["name"] != "None":
        #check if user give consent response
        try:
            dateRequestConcent: dict
            dateRequestConcent = requests.post(f"{BASE_URL}/consent/get_response",
                                               json={"user_tg_id": message.from_user.id}).json()
        except Exception as e:
            log_error(e)
            dateRequestConcent = {"action": "technical maintenance"}
        if dateRequestConcent["action"] == "success" and dateRequestConcent["data"]["response"] == 1:
            dataAboutUser[message.from_user.id]["user_id"] = dateRequest["id"]
            dataAboutUser[message.from_user.id]["user_name"] = dateRequest["name"]
            await MenuUser.start_state.set()
            await bot.send_message(message.from_user.id, f'{text_1.t_welcome}', reply_markup=GeneralKeyboards.mainMenu)
    elif dateRequest["action"] == "technical maintenance":
        await bot.send_sticker(message.from_user.id, sticker=open("data/png/file_131068229.png", 'rb'))
        await bot.send_message(message.from_user.id, text_1.t_mistake)
        ts(1)
        await bot.send_message(message.from_user.id, text_2.t_technical_maintenance, reply_markup=GeneralKeyboards.single_btn_command_menu)
    else:
        await UserState.start_register.set()
        await bot.send_sticker(message.from_user.id, sticker=open("data/png/file_131068231.png", 'rb'))
        await bot.send_message(message.from_user.id, text_1.t_start_1)
        ts(1)
        await bot.send_message(message.from_user.id, text_1.t_start_2)
        ts(1)
        await bot.send_message(message.from_user.id, text_1.t_start_3, reply_markup=GeneralKeyboards.group_startMenu)


async def getTripsByDirection(message: types.Message):
    await GetTrips.get_trips_by_direction.set()
    await bot.send_message(message.from_user.id, "Выбери направление:", reply_markup=direction_keyboard())


async def getDrivers(message: types.Message):
    try:
        isBecomeDriverData = requests.get(f"{BASE_URL}/get_drivers/by_status",
                                           json={"status": 1}).json()
        driversDataList = []
        for i in isBecomeDriverData["data"]:
            try:
                driverData = requests.post(f"{BASE_URL}/getusers",
                                          json={"id": i["id_user"]}).json()
                driversDataList.append(driverData['data'])
            except Exception as e:
                log_error(e)
    except Exception as e:
        log_error(e)

    if len(driversDataList) > 0:
        answer = generate_new_str_for_drivers(driversDataList)
        await bot.send_message(message.from_user.id, "Потенциальные водители:\n" + answer,
                               reply_markup=GeneralKeyboards.mainMenu)
    else:
        await bot.send_message(message.from_user.id, "Потенциальных водителей не нашлось(((",
                               reply_markup=GeneralKeyboards.mainMenu)




async def startRegister(message: types.Message):
    """
    startRegister function

    Intermediate command

    :param message: The message containing the user's input
    :type message: types.Message

    Returns:
    - None (sends messages and updates the user state)
    """

    # Checking whether the user has selected
    if message.text == "О сервисе":
        await MenuAbout.start_state.set()
        await bot.send_message(message.from_user.id, text_1.t_time, reply_markup=GeneralKeyboards.group_aboutServiceMenu)
    elif message.text == "Зарегистрироваться! 🐣":
        await AgreementUser.get_user_info.set()
        await bot.send_message(message.from_user.id, f'{text_1.t_agreement_1}',
                               reply_markup=GeneralKeyboards.group_agreement)
        await bot.send_message(message.from_user.id, f'{text_1.t_agreement_4}',
                               reply_markup=keyboards.inlineKeyboards.UserAgreement)
    else:
        # Foolproof
        await bot.send_message(message.from_user.id, text_1.t_foolproof_buttons, reply_markup=GeneralKeyboards.group_startMenu)


# User agreement
async def user_agreement(message: types.Message):
    global dataAboutUser
    if message.text == "Согласиться":
        try:
            dateRequest: dict
            dateRequest = requests.post(
                f"{BASE_URL}/consent/save_response", json={"user_tg_id": dataAboutUser[message.from_user.id]["user_tg_id"],
                                                           "response": 1}).json()
        except Exception as e:
            log_error(e)
            await bot.send_sticker(message.from_user.id, sticker=open("data/png/file_131068229.png", 'rb'))
            await bot.send_message(message.from_user.id, text_1.t_mistake)
        if dateRequest["action"] == "success":
            await UserState.get_dateAboutUser_name.set()
            ts(1)
            await bot.send_message(message.from_user.id, text_1.t_reg_name_1)
            ts(1)
            await bot.send_message(message.from_user.id, text_1.t_reg_name_2)
    else:
        await bot.send_message(message.from_user.id, text_1.t_foolproof_buttons)
        await UserState.start_register.set()





# _ _ _ Start_register _ _ _


async def first_register_name(message: types.Message, state: FSMContext):
    """
    first_register_name function

    Get user name

    Parameters:
    - message: The message containing the user's input
    Type: types.Message
    - state: The state of the user
    Type: FSMContext

    Global Variables:
    - dataAboutUser: A dictionary containing user data
    Type: dict

    Returns:
    - None (sends messages and updates the user state)
    """

    # Initialize global variables
    global dataAboutUser

    # Checking for a fool
    if foolproofCyrillic(message.text):
        # Initialize user data dictionaries
        dataAboutUser[message.from_user.id]["user_name"] = message.text
        await bot.send_message(message.from_user.id, text_1.t_reg_name_3)
        await UserState.get_dateAboutUser_surname.set()
    else:
        # Foolproof
        await bot.send_message(message.from_user.id, text_1.t_foolproof_correct_data)


async def first_register_surname(message: types.Message, state: FSMContext):
    """
    first_register_surname function

    Get user surname

    Parameters:
    - message: The message containing the user's input
    Type: types.Message
    - state: The state of the user
    Type: FSMContext

    Global Variables:
    - dataAboutUser: A dictionary containing user data
    Type: dict

    Returns:
    - None (sends messages and updates the user state)
    """
    global dataAboutUser

    # Checking for a fool
    if foolproofCyrillic(message.text):

        # Initialize user data dictionaries
        dataAboutUser[message.from_user.id]["user_surname"] = message.text
        await bot.send_message(message.from_user.id, text_1.t_reg_name_4, reply_markup=GeneralKeyboards.single_send_number)
        await UserState.get_dateAboutUser_number.set()
    else:
        # Foolproof
        await bot.send_message(message.from_user.id, text_1.t_foolproof_correct_data)


async def first_register_number(message: types.Message, state: FSMContext):
    """
    first_register_number function

    Get user number

    Parameters:
    - message: The message containing the user's input
    Type: types.Message
    - state: The state of the user
    Type: FSMContext

    Global Variables:
    - dataAboutUser: A dictionary containing user data
    Type: dict
    - BASE_URL: The base URL for the requests
    Type: str

    Returns:
    - None (updates the user state and sends a message)
    """
    global dataAboutUser
    phone_number = 0

    if message.contact is not None and message.contact.phone_number is not None:
        phone_number = message.contact.phone_number
    elif foolproofPhoneNumber(message.text):
        phone_number = message.text
    else:
        # Foolproof
        await bot.send_message(message.from_user.id, text_1.t_foolproof_correct_data)

    # Checking for a fool
    if phone_number != 0:
        # Initialize user data dictionaries
        dataAboutUser[message.from_user.id]["user_number"] = phone_number
        try:
            zapros = {"name": dataAboutUser[message.from_user.id]["user_name"], "numb": dataAboutUser[message.from_user.id]["user_number"],
                      "id_tg": dataAboutUser[message.from_user.id]["user_tg_id"], "surname": dataAboutUser[message.from_user.id]["user_surname"]}
            dateRequest = requests.post(
                f"{BASE_URL}/registrations", json=zapros).json()["id"]
            dataAboutUser[message.from_user.id]["user_id"] = dateRequest
            driver_set = {"id_user": dataAboutUser[message.from_user.id]["user_id"], "status": 0}
            dr_data = requests.post(
                f"{BASE_URL}/check_drivers/save_drivers", json=driver_set).json()
            await MenuUser.start_state.set()
            await bot.send_sticker(message.from_user.id, sticker=open("data/png/file_131068230.png", 'rb'))
            await bot.send_message(message.from_user.id, text_1.t_first_welcome, reply_markup=GeneralKeyboards.mainMenu)
        except Exception as e:
            log_error(e)
            if dateRequest["action"] == "errorData":
                await bot.send_sticker(message.from_user.id, sticker=open("data/png/file_131068229.png", 'rb'))
                await bot.send_message(message.from_user.id, text_1.t_mistake)
                ts(1)
                await bot.send_message(message.from_user.id, text_2.t_technical_maintenance, reply_markup=GeneralKeyboards.single_btn_command_menu)


# _ _ _ MENU _ _ _


async def mainMenu(message: types.Message, state: FSMContext):
    global dataAboutUser, dataAboutTrip, dataAboutCar

    try:
        checkAccounting = dataAboutUser[message.from_user.id]
    except:
        dataAboutUser[message.from_user.id] = {
            "user_tg_id": message.from_user.id}
        dataAboutTrip[message.from_user.id] = {
            "user_tg_id": message.from_user.id}
        dataAboutCar[message.from_user.id] = {
            "user_tg_id": message.from_user.id}
        try:
            dateRequest: dict
            dateRequest = requests.post(
                f"{BASE_URL}/checkuser", json={"id_tg": dataAboutUser[message.from_user.id]["user_tg_id"]}).json()
        except Exception as e:
            log_error(e)
            dateRequest = {"action": "technical maintenance"}
        if dateRequest["action"] == "success" and dateRequest["name"] != "None":
            dataAboutUser[message.from_user.id]["user_id"] = dateRequest["id"]
            dataAboutUser[message.from_user.id]["user_name"] = dateRequest["name"]
        else:
            await bot.send_sticker(message.from_user.id, sticker=open("data/png/file_131068229.png", 'rb'))
            await bot.send_message(message.from_user.id, text_1.t_mistake)
            ts(1)
            await bot.send_message(message.from_user.id, text_2.t_technical_maintenance, reply_markup=GeneralKeyboards.single_btn_command_menu)
            return
    # Register user in the service
    """
    mainMenu function

    A function for determining the start of a specific menu section using the start state and processing user input.

    Parameters:
    - message: The message containing the user's input
    Type: types.Message
    - state: The state of the user
    Type: FSMContext

    Returns:
    - None (sends messages and updates the user state)
    """

    # Depending on the user input, perform the appropriate action
    if message.text == "Профиль":
        await myProfileCommandRegisteredFunction(message, state)
    elif message.text == "Мои поездки":
        await myTripsCommandRegisteredFunction(message, state)
    elif message.text == "Поддержка":
        await bot.send_message(message.from_user.id, text_2.t_support, reply_markup=supportkb)
    elif message.text == "О сервисе":
        await MenuUser.go_to_about.set()
        await bot.send_message(message.from_user.id, text_1.t_about, reply_markup=GeneralKeyboards.group_aboutServiceMenuRegistered)
    elif message.text == "Создать поездку":
        await CreateTrip.start_creating.set()
        await bot.send_message(message.from_user.id, text_3.t_go)
        await bot.send_message(message.from_user.id, text_3.t_get_dateAboutUser_typeOfMembers, reply_markup=GeneralKeyboards.group_status)

        # await MenuUser.go_CreateTrip.set()
        # await bot.send_message(message.from_user.id, text_1.t_time, reply_markup=GeneralKeyboards.single_btn_next)
    else:
        # Foolproof
        await bot.send_message(message.from_user.id, text_1.t_foolproof_buttons, reply_markup=GeneralKeyboards.mainMenu)


async def aboutCommandRegistered(message: types.Message):
    """
    About service

    The function processes requests from the "Service" section and sends information about the selected option. It also allows the user to return to the main menu.

    Parameters:
    - message: The message containing the user's input
    Type: types.Message

    Global Variables:
    - dataAboutUser: A dictionary containing user data
    Type: dict

    Returns:
    - None (sends messages and updates the user state)
    """
    # Initialize global variables
    global dataAboutUser

    # Depending on the user input, perform the appropriate action
    if message.text == "F.A.Q.":
        await bot.send_message(message.from_user.id, text_2.t_FAQ)
    elif message.text == "Правила сервиса":
        await bot.send_message(message.from_user.id, text_2.t_rules)
    elif message.text == "Описание":
        await bot.send_message(message.from_user.id, text_2.t_about)
    elif message.text == "Вернуться в главное меню":
        await MenuUser.start_state.set()
        await bot.send_message(message.from_user.id, f'{text_1.t_welcome}', reply_markup=GeneralKeyboards.mainMenu)
    else:
        await MenuUser.start_state.set()
        # Foolproof
        await bot.send_message(message.from_user.id, text_1.t_foolproof_buttons, reply_markup=GeneralKeyboards.mainMenu)


async def become_driver_end(message: types.Message, state: FSMContext):
    if message.text == "В главное меню":
        await MenuUser.start_state.set()
        await bot.send_message(message.from_user.id, f'{text_1.t_welcome}', reply_markup=GeneralKeyboards.mainMenu)


async def myProfileCommandRegistered(message: types.Message, state: FSMContext):

    """
    My profile info

    The function handles requests from the "Profile" section. Created to further
    increase the functionality, namely: the ability to edit the profile

    :Returns to the main menu, sending information about a section
    """

    await MenuUser.start_state.set()
    if message.text == "Вернуться в главное меню":
        await bot.send_message(message.from_user.id, f'{text_1.t_welcome}', reply_markup=GeneralKeyboards.mainMenu)
    elif message.text == "Стать водителем":
        await bot.send_message(message.from_user.id, f'{text_1.t_become_1}',
                               reply_markup=GeneralKeyboards.single_btn_become_end)
        await bot.send_message(message.from_user.id, f'{text_1.t_become_2}',
                               reply_markup=keyboards.inlineKeyboards.becomekb)
        await BecomeDriver.start_become_dr.set()
    elif message.text == 'Текущий баланс':
        # trying to get user balance
        try:
            balance: dict
            balance = requests.post(
            f"{BASE_URL}/balance/getusers", json={"user_id": dataAboutUser[message.from_user.id]["user_id"]}).json()["balance"]

        except Exception as e:
            log_error(e)
        # showing user balance if it's exist
        balance_text = f'Ваш баланс: {balance} ₽'
        await bot.send_message(message.from_user.id, balance_text, reply_markup=GeneralKeyboards.mainMenu)
    elif message.text == 'Пополнить баланс':
        await ProfileMenu.set_top_up_balance.set()
        await bot.send_message(message.from_user.id, 'Выбери сумму пополнения', reply_to_message_id=message.message_id,
                               reply_markup=SimpleKeyboardsForReplenishBalance.top_up_menu)
    else:
        # Foolproof
        await bot.send_message(message.from_user.id, text_1.t_foolproof_buttons, reply_markup=GeneralKeyboards.mainMenu)


async def myProfileCommandRegisteredFunction(message: types.Message, state: FSMContext):
    """
    My profile info Function

    Function - Compact algorithm packaging for the "Profile" section function

    :param message: a class representing a user's message in a telegram bot
    :type message: types.Message
    :param state: For the possibility of further upgrade of the bot
    :type state: FSMContext
    :send_message: User Information
    :type: Text
    """
    global dataAboutUser, dataAboutTrip, dataAboutCar
    # Connection.accessing the database using an exception
    try:
        userData = requests.post(
            f"{BASE_URL}/getusers", json={"id": f'{dataAboutUser[message.from_user.id]["user_id"]}'}).json()
        driver_state = requests.post(
                f"{BASE_URL}/check_drivers/get_drivers",
                json={"id_user": f'{dataAboutUser[message.from_user.id]["user_id"]}'}).json()['data']['status']
    except Exception as e:  # If an exception occurs, writes error data
        log_error(e)
        some_info = "technical maintenance"
    if userData["action"] == "success":
        # Output of user data to the bot
        await MenuUser.set_profileInfo.set()
        userData = userData["data"]
        if driver_state == 1:
            await bot.send_message(message.from_user.id, f"Имя: {userData['name']}\n"
                               f"Фамилия: {userData['surname']}\n"
                               f"Номер: {userData['numb']}\n", reply_markup=GeneralKeyboards.group_profileMenu_1)
        else:
            await bot.send_message(message.from_user.id, f"Имя: {userData['name']}\n"
                                                         f"Фамилия: {userData['surname']}\n"
                                                         f"Номер: {userData['numb']}\n",
                                   reply_markup=GeneralKeyboards.group_profileMenu)
    elif userData["action"] == "technical maintenance":
        # Output of the text about the occurrence of an error in the database to the user
        await bot.send_sticker(message.from_user.id, sticker=open("data/png/file_131068229.png", 'rb'))
        await bot.send_message(message.from_user.id, text_1.t_mistake)
        ts(1)
        await bot.send_message(message.from_user.id, text_2.t_technical_maintenance, reply_markup=GeneralKeyboards.single_btn_command_menu)


async def myTripsCommandRegistered(message: types.Message, state: FSMContext):
    """
    My trips info

    The function handles requests from the "My Trips" section. Created to further
    expand the functionality, namely: the ability to edit trips

    :Returns to the main menu, sending information about a section
    """
    await MenuUser.start_state.set()
    if message.text != "Вернуться в главное меню":
        # Foolproof
        await bot.send_message(message.from_user.id, text_1.t_foolproof_buttons, reply_markup=GeneralKeyboards.mainMenu)
    else:
        await bot.send_message(message.from_user.id, f'{text_1.t_welcome}', reply_markup=GeneralKeyboards.mainMenu)


async def myTripsCommandRegisteredFunction(message: types.Message, state: FSMContext):
    """
    My trips info Function

    Function - Compact algorithm packaging for the "My Trips" section function

    :param message: a class representing a user's message in a telegram bot
    :type message: types.Message
    :param state: For the possibility of further upgrade of the bot
    :type state: FSMContext
    :send_message: Information about trips
    :type: Text
    """
    global dataAboutUser, dataAboutTrip, dataAboutCar
    # Connection.accessing the database using an exception
    try:
        userData = requests.post(f"{BASE_URL}/gettrips/trips", json={
            "id": f'{dataAboutUser[message.from_user.id]["user_id"]}'}).json()
    except Exception as e:
        log_error(e)
        userData = {"action": "technical maintenance"}
    try:
        if userData["action"] == "technical maintenance":
            # Output of the text about the occurrence of an error in the database to the user
            await bot.send_sticker(message.from_user.id, sticker=open("data/png/file_131068229.png", 'rb'))
            await bot.send_message(message.from_user.id, text_1.t_mistake)
            ts(1)
            await bot.send_message(message.from_user.id, text_2.t_technical_maintenance,
                                   reply_markup=GeneralKeyboards.single_btn_command_menu)
        elif userData["action"] == "success":
            # Output of user data to the bot
            await CheckTripsMenu.start_state.set()
            userData = userData["data"]
            newStr = generate_new_str(userData)
            await bot.send_message(message.from_user.id, "О каких поездках хочешь узнать?",
                                   reply_markup=GeneralKeyboards.group_check_trips_menu)

    except Exception as e:
        await MenuUser.set_myTrips.set()
        await bot.send_message(message.from_user.id, text_2.t_no_active_trips,
                               reply_markup=GeneralKeyboards.single_btn_main)


async def check_my_trips(message: types.Message, state: FSMContext):
    """
    Check My Trips Function

    Function - Checks and displays the user's current or past trips based on the input message

    :param message: a class representing a user's message in a telegram bot
    :type message: types.Message
    :param state: For the possibility of further upgrade of the bot
    :type state: FSMContext
    :send_message: Information about trips
    :type: Text
    """
    global last_trip_id
    current_datetime = datetime.now()
    if message.text == "Текущие поездки":
        userData = requests.post(f"{BASE_URL}/gettrips/trips", json={
            "id": f'{dataAboutUser[message.from_user.id]["user_id"]}'}).json()
        data_list = create_list_of_trips(userData['data'], 10, 1)
        await MenuUser.start_state.set()
        if len(data_list) > 0:
            await bot.send_message(message.from_user.id, generate_new_str(data_list),
                                   reply_markup=GeneralKeyboards.mainMenu)
        else:
            await bot.send_message(message.from_user.id, "У вас нет актуальных поездок(((",
                                   reply_markup=GeneralKeyboards.mainMenu)

    elif message.text == "Прошлые поездки":
        userData = requests.post(f"{BASE_URL}/gettrips/trips", json={
            "id": f'{dataAboutUser[message.from_user.id]["user_id"]}'}).json()
        data_list = create_list_of_trips(userData['data'], 10, 0)
        await MenuUser.start_state.set()
        if len(data_list) > 0:
            await bot.send_message(message.from_user.id, generate_new_str(data_list),
                                   reply_markup=GeneralKeyboards.mainMenu)
        else:
            await bot.send_message(message.from_user.id, "Вы еще не совершали поездок(((",
                                   reply_markup=GeneralKeyboards.mainMenu)

    elif message.text == "Оставить отзыв":
        await bot.send_message(message.from_user.id, "Оставить отзыв можно только на послеюнюю поездку")

        tripsData = requests.post(f"{BASE_URL}/gettrips/trips", json={
            "id": f'{dataAboutUser[message.from_user.id]["user_id"]}'}).json()
        data_list = create_list_of_trips(tripsData['data'], 120, 2)
        if len(data_list) > 0:
            sorted_data = sorted(data_list, key=lambda x: x['tripstimes'], reverse=True)
            last_trip = []
            last_trip.append(sorted_data[0])
            last_trip_id = last_trip[0]['id_trip']

            await LeaveReview.start_state.set()
            await bot.send_message(message.from_user.id, f"{generate_new_str(last_trip)[3:]}",
                                   reply_markup=ReplyKeyboardRemove())
            await bot.send_message(message.from_user.id, "Отправь мне текстом свой отзыв на эту поездку!")
        else:
            await MenuUser.start_state.set()
            await bot.send_message(message.from_user.id, "Вы еще не совершали поездок(((",
                                   reply_markup=GeneralKeyboards.mainMenu)

    elif message.text == "Вернуться в главное меню":
        await MenuUser.start_state.set()
        await bot.send_message(message.from_user.id, f'{text_1.t_welcome}', reply_markup=GeneralKeyboards.mainMenu)

    else:
        await MenuUser.start_state.set()
        await bot.send_message(message.from_user.id, text_1.t_foolproof_buttons, reply_markup=GeneralKeyboards.mainMenu)


async def leave_review(message: types.Message, state: FSMContext):
    global last_trip_id, review_text
    review_text = message.text
    await LeaveReview.set_confirmation.set()
    await bot.send_message(message.from_user.id, f'Ты точно хочешь оставить этот отзыв?\n\n"{review_text}"', reply_markup=GeneralKeyboards.group_yesNo)


async def leave_review_confirmation(message: types.Message, state: FSMContext):
    global last_trip_id, review_text
    if message.text == "Да":
        try:
            requests.post(f"{BASE_URL}/reviews/create",
                          json={"id_trip": last_trip_id, "review_text": review_text})
            await bot.send_message(message.from_user.id, "Отзыв успешно отправлен!")
        except Exception as e:
            log_error(e)
            print(e)
        await MenuUser.start_state.set()
        await bot.send_message(message.from_user.id, text_1.t_welcome, reply_markup=GeneralKeyboards.mainMenu)
    elif message.text == "Нет":
        await MenuUser.start_state.set()
        await bot.send_message(message.from_user.id, "Отправка отзыва отменена", reply_markup=GeneralKeyboards.mainMenu)
    else:
        await bot.send_message(message.from_user.id, f'{text_1.t_foolproof_buttons}')
        await bot.send_message(message.from_user.id, f'Ты точно хочешь оставить этот отзыв?\n\n"{review_text}"',
                               reply_markup=GeneralKeyboards.group_yesNo)


# _ _ _ TRIPS _ _ _


# async def createTripForUser(message : types.Message):
#     """
#     Create a trip

#     Function for starting the trip creation process.

#     Parameters:
#     - message: The message containing the user's input
#     Type: types.Message

#     Returns:
#     - None (sends messages and updates the user state)
#     """
#     await CreateTrip.start_creating.set()
#     await bot.send_message(message.from_user.id, text_3.t_go)
#     await bot.send_message(message.from_user.id, text_3.t_get_dateAboutUser_typeOfMembers, reply_markup=GeneralKeyboards.group_status)


async def createTripForUser_typeOfMembers(message: types.Message):
    """
    Create trip for user & type of members

    Function for handling the selection of the type of members for the trip.

    Parameters:
    - message: The message containing the user's input
    Type: types.Message

    Global Variables:
    - dataAboutUser: A dictionary containing user data
    Type: dict
    - dataAboutTrip: A dictionary containing trip data
    Type: dict
    - dataAboutCar: A dictionary containing car data
    Type: dict
    - BASE_URL: The base URL for the requests
    Type: str

    Returns:
    - None (sends messages and updates the user state)
    """
    global dataAboutUser, dataAboutTrip, dataAboutCar
    check = requests.post(f"{BASE_URL}/check_drivers/get_drivers", json={"id_user": dataAboutUser[message.from_user.id]["user_id"]}).json()["data"]["status"]
    if message.text == "Водитель" and check == 1:
        dataAboutTrip[message.from_user.id]["typeOfMembers"] = "driver"
        try:
            userData = requests.post(f"{BASE_URL}/gettrips/drivers", json={
                                     "user_id": dataAboutUser[message.from_user.id]["user_id"]}).json()
        except Exception as e:
            log_error(e)
            userData = {"action": "technical maintenance"}
        if userData["action"] == "technical maintenance":
            await bot.send_sticker(message.from_user.id, sticker=open("data/png/file_131    068229.png", 'rb'))
            await bot.send_message(message.from_user.id, text_1.t_mistake)
            ts(1)
            await bot.send_message(message.from_user.id, text_2.t_technical_maintenance, reply_markup=GeneralKeyboards.single_btn_command_menu)
        elif len(userData["data"]) > 0:
            userData["data"] = userData["data"][0]
            dataAboutCar[message.from_user.id]["carData"] = userData["data"]
            await bot.send_message(message.from_user.id, text_3.t_get_dateAboutUser_carData, reply_markup=GeneralKeyboards.group_yesNo)
            dataAboutCar[message.from_user.id]["car_id"] = userData["data"]["car_id"]
            await CreateTrip.get_dateAboutUser_typeOfMembers.set()
            await bot.send_message(message.from_user.id, f'Бренд: {userData["data"]["brand"]}\nЦвет: {userData["data"]["colour"]}\nНомера: {userData["data"]["numbcar"]}')
        else:
            await CreateTrip.get_tripNumberOfPassengers.set()
            dataAboutCar[message.from_user.id]["check_"] = 0
            await bot.send_message(message.from_user.id, text_3.t_get_tripNumberOfPassengers)
    elif message.text == "Пассажир":
        data = inlineKeyboards.GenerationOfInlineButtons_calendar()
        dataAboutTrip[message.from_user.id]["typeOfMembers"] = "passenger"
        await CreateTrip.get_dateAboutUser_carData.set()
        await bot.send_message(message.from_user.id, text_3.t_get_dateAbout_tripDates, reply_markup=data[2])
        dataAboutTrip[message.from_user.id]["tripNumberOfPassengers"] = 0
        dataAboutTrip[message.from_user.id]["page_number"] = [
            data[0], data[1], data[3], data[4]]
    elif check == 0:
        await bot.send_message(message.from_user.id, text_1.t_set_driver, reply_markup=GeneralKeyboards.group_status)
    else:
        # Foolproof
        await bot.send_message(message.from_user.id, text_1.t_foolproof_buttons, reply_markup=GeneralKeyboards.group_status)


async def choose_direction_for_search(callback_query: types.CallbackQuery, state: FSMContext):
    callback_data = callback_query.data
    print('callback_data', callback_data)
    directions = {
        "voenC": "Военвед - Центр",
        "suvC": "Суворовский - Центр",
        "sevC": "Северный - Центр",
        "selC": "Сельмаш - Центр",
        "zapC": "Западный - Центр",
        "cVoen": "Центр - Военвед",
        "cSuv": "Центр - Суворовский",
        "cSev": "Центр - Северный",
        "cSel": "Центр - Сельмаш",
        "cZap": "Центр - Западный"
    }
    direction_name = directions.get(callback_data, "")
    try:
        tripsData = requests.get(f"{BASE_URL}/gettrips/getTripsByDirection", json={"direction_name": f'{direction_name}'}).json()['data']
    except Exception as e:
        print(e)

    if len(tripsData) > 0:
        newStr = generate_new_str(tripsData)
        await MenuUser.start_state.set()
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, f'Все поездки по направлению "{direction_name}"')
        await bot.send_message(callback_query.from_user.id, newStr, reply_markup=GeneralKeyboards.mainMenu)
    else:
        await MenuUser.start_state.set()
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, f'По направлению "{direction_name}" поездок не нашлось(((', reply_markup=GeneralKeyboards.mainMenu)


# _ _ _ Creating a trip new version _ _ _

async def choose_direction(callback_query: types.CallbackQuery, state: FSMContext):
    global dataAboutTrip
    callback_data = callback_query.data
    directions = {
        "voenC": "Военвед - Центр",
        "suvC": "Суворовский - Центр",
        "sevC": "Северный - Центр",
        "selC": "Сельмаш - Центр",
        "zapC": "Западный - Центр",
        "cVoen": "Центр - Военвед",
        "cSuv": "Центр - Суворовский",
        "cSev": "Центр - Северный",
        "cSel": "Центр - Сельмаш",
        "cZap": "Центр - Западный"
    }
    direction_name = directions.get(callback_data, "")

    dataAboutTrip[callback_query.from_user.id]["directionName"] = direction_name
    route_numbers = DirectionRoutesPoints.get_number_of_routes_by_direction(direction_name)
    routes_text = ""
    for i in range(1, route_numbers + 1):
        routes_text += f'{i} - {DirectionRoutesPoints.get_route_by_direction(dataAboutTrip[callback_query.from_user.id]["directionName"], i)["link"]}\n\n'
    await bot.send_message(callback_query.from_user.id, f"У нас есть такие маршруты:\n\n{routes_text}", reply_markup=route_keyboard(callback_data))
    await CreateTripPassenger.next()


async def choose_route(callback_query: types.CallbackQuery, state: FSMContext):
    global dataAboutTrip
    callback_data = callback_query.data
    async with state.proxy() as data:
        data['marshrut'] = callback_data
        dataAboutTrip[callback_query.from_user.id]["routeNumber"] = extract_number(callback_data)
    await CreateTripPassenger.next()
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text='Откуда:',
                                reply_markup=point_A_keyboard(route=callback_data))


async def createTrip_pointA(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Create trip for user & trip point A

    This function handles the entry of trip point A by the user.
    It updates the tripPointA in the dataAboutTrip dictionary, sets the user state to set_pointB,
    and edit keyboard to select the trip point B.

    :param callback_query: The call containing the user's input
    :type callback_query: types.CallbackQuery
    :param state: The FSMContext that contains the state of the FSM
    :type state: FSMContext
    """
    global dataAboutTrip
    call_data = callback_query.data
    async with state.proxy() as data:
        data['tochka1'] = call_data
        dataAboutTrip[callback_query.from_user.id]["pointA"] = int(callback_query.data)
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text='Куда:',
                                    reply_markup=point_B_keyboard(route=data['marshrut'], pointA=int(call_data) + 1))
    await CreateTripPassenger.next()


async def createTrip_pointB(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Create trip for user & trip point B

    This function handles the entry of trip point B by the user.
    It updates the tripPointB in the dataAboutTrip dictionary, sets the user state to MenuUser.start_state,
    and edit keyboard to confirm or decline trip.

    :param callback_query: The call containing the user's input
    :type callback_query: types.CallbackQuery
    :param state: The FSMContext that contains the state of the FSM
    :type state: FSMContext
    """
    global dataAboutTrip
    call_data = callback_query.data
    async with state.proxy() as data:
        data['tochka2'] = call_data
        dataAboutTrip[callback_query.from_user.id]["pointB"] = int(callback_query.data)
        typeOfMembers = "Пассажир" if dataAboutTrip[callback_query.from_user.id][
                        "typeOfMembers"] == "passenger" else "Водитель"
        text=f"""Тип участника: {typeOfMembers}
            Направление: {dataAboutTrip[callback_query.from_user.id]['directionName']}
            Маршрут: {dataAboutTrip[callback_query.from_user.id]['routeNumber']}
            Откуда: {DirectionRoutesPoints.get_point_by_direction_and_route(dataAboutTrip[callback_query.from_user.id]['directionName'], 
                                                                            dataAboutTrip[callback_query.from_user.id]["routeNumber"], 
                                                                            dataAboutTrip[callback_query.from_user.id]["pointA"])}
            Куда: {DirectionRoutesPoints.get_point_by_direction_and_route(dataAboutTrip[callback_query.from_user.id]['directionName'], 
                                                                            dataAboutTrip[callback_query.from_user.id]["routeNumber"], 
                                                                            dataAboutTrip[callback_query.from_user.id]["pointB"])}
            Дата и время поездки: {format_date_time(dataAboutTrip[callback_query.from_user.id]["tripDates"])}  {format_date_time(dataAboutTrip[callback_query.from_user.id]["tripTimes"])}"""

        #If member type is passenger we show him cost of his trip
        if typeOfMembers == 'Водитель':
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text = text, reply_markup=None)
        else:
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text = text + f'''{calculate_trip_cost(
                dataAboutTrip[callback_query.from_user.id]["pointA"], dataAboutTrip[callback_query.from_user.id]["pointB"])}''', reply_markup=None)

    await CreateTripPassenger.set_confirmation.set()
    # await bot.send_message(callback_query.from_user.id, text_1.t_welcome, reply_markup=GeneralKeyboards.mainMenu)
    await bot.send_message(callback_query.from_user.id, "Все верно?", reply_markup=GeneralKeyboards.group_yesNo)


# _ _ _ Creating a trip _ _ _
async def functionFoolproof(message: types.Message):
    """
    functionFoolproof

    Asks to use the suggested buttons

    Returns:
    - None (sends messages)
    """
    await bot.send_message(message.from_user.id, text_1.t_foolproof_buttons)


async def handle_title_button(callback_query: types.CallbackQuery):
    """
    Handle the title button callback query

    This function sends message

    :param callback_query: The callback query
    :type callback_query: types.CallbackQuery
    """
    await callback_query.answer("Мы уже разрабатываем новые функции 😊")


async def handle_cancel_button(callback_query: types.CallbackQuery):
    """
    Handle the cancel button callback query

    This function sets the user state to start_state and sends a welcome message with the main menu

    :param callback_query: The callback query
    :type callback_query: types.CallbackQuery
    """
    await callback_query.answer("")
    await MenuUser.start_state.set()
    await bot.send_message(callback_query.from_user.id, f'{text_1.t_welcome}', reply_markup=GeneralKeyboards.mainMenu)


async def createTripForUser_carData(message: types.Message):
    """
    Create trip for user & car data

    Function for handling the selection of car data by the user.

    Parameters:
    - message: The message containing the user's input
    Type: types.Message

    Global Variables:
    - dataAboutCar: A dictionary containing car data
    Type: dict

    Returns:
    - None (sends messages and updates the user state)
    """
    global dataAboutCar
    await CreateTrip.get_tripNumberOfPassengers.set()
    await bot.send_message(message.from_user.id, text_3.t_get_tripNumberOfPassengers)
    dataAboutCar[message.from_user.id]["check_"] = 1 if message.text == "Да" else 0


async def createTripForUser_tripNumberOfPassengers(message: types.Message):
    """
    Create trip for user & number of passengers

    Function for handling the selection of the number of passengers for the trip.

    Parameters:
    - message: The message containing the user's input
    Type: types.Message

    Global Variables:
    - dataAboutTrip: A dictionary containing trip data
    Type: dict
    - dataAboutCar: A dictionary containing car data
    Type: dict

    Returns:
    - None (sends messages and updates the user state)
    """
    global dataAboutTrip, dataAboutCar

    try:
        if int(message.text) >= 0 and int(message.text) <= 4:  # Maximum number of passengers
            dataAboutTrip[message.from_user.id]["tripNumberOfPassengers"] = int(message.text)
            if dataAboutCar[message.from_user.id]["check_"] == 1:
                data = inlineKeyboards.GenerationOfInlineButtons_calendar()
                await CreateTrip.get_dateAboutUser_carData.set()
                await bot.send_message(message.from_user.id, text_3.t_get_dateAbout_tripDates, reply_markup=data[2])
                dataAboutTrip[message.from_user.id]["page_number"] = [
                    data[0], data[1], data[3], data[4]]

            else:
                await RecordingInformationAboutCar.start_state.set()
                dataAboutCar[message.from_user.id]["page_numberBrands"] = 0
                dataAboutCar[message.from_user.id]["page_numberModels"] = 0
                await bot.send_message(message.from_user.id, text_3.t_noCarInTheDataBase_carBrand, reply_markup=GenerationOfInlineButtons(general_data.cars.brends, "Бренды")[0])
        else:
            # Foolproof
            await bot.send_message(message.from_user.id, text_1.t_foolproof_correct_data)
    except Exception as e:
        # Foolproof
        await bot.send_message(message.from_user.id, text_1.t_foolproof_correct_data)


# _ _ _ Recording machine data _ _ _
async def handle_cancel_button(callback_query: types.CallbackQuery):
    """
    Handle the cancel button callback query

    This function sets the user state to start_state and sends a welcome message with the main menu

    :param callback_query: The callback query
    :type callback_query: types.CallbackQuery
    """
    await callback_query.answer("")
    await MenuUser.start_state.set()
    await bot.send_message(callback_query.from_user.id, f'{text_1.t_welcome}', reply_markup=GeneralKeyboards.mainMenu)


async def handle_prev_button(callback_query: types.CallbackQuery):
    """
    Handle the previous button callback query

    This function handles the pagination for car brands and updates the inline keyboard markup with the previous page

    :param callback_query: The callback query
    :type callback_query: types.CallbackQuery
    """
    global dataAboutCar
    await callback_query.answer("")
    data = GenerationOfInlineButtons(general_data.cars.brends, "Бренды",
                                     page_number=dataAboutCar[callback_query.from_user.id]["page_numberBrands"] - 1)
    if data != -2:
        dataAboutCar[callback_query.from_user.id]["page_numberBrands"] = data[1]
        dataAboutCar[callback_query.from_user.id]["page_numberModels"] = 0
        await callback_query.message.edit_reply_markup(data[0])


async def handle_next_button(callback_query: types.CallbackQuery):
    """
    Handle the next button callback query

    This function handles the pagination for car brands and updates the inline keyboard markup with the next page

    :param callback_query: The callback query
    :type callback_query: types.CallbackQuery
    """
    global dataAboutCar
    await callback_query.answer("")
    data = GenerationOfInlineButtons(general_data.cars.brends, "Бренды",
                                     page_number=dataAboutCar[callback_query.from_user.id]["page_numberBrands"] + 1)
    if data != -2:
        dataAboutCar[callback_query.from_user.id]["page_numberBrands"] = data[1]
        dataAboutCar[callback_query.from_user.id]["page_numberModels"] = 0
        await callback_query.message.edit_reply_markup(data[0])


async def handle_brand_button(callback_query: types.CallbackQuery):
    """
    Handle the brand button callback query

    This function handles the selection of a car brand and updates the carBrand in the dataAboutCar dictionary.
    It also sets the user state to start_state_model and sends a message to select the car model.

    :param callback_query: The callback query
    :type callback_query: types.CallbackQuery
    """
    await callback_query.answer("")
    global dataAboutCar
    dataAboutCar[callback_query.from_user.id]["carBrand"] = callback_query.data
    await RecordingInformationAboutCar.start_state_model.set()
    await callback_query.message.edit_text(text_3.t_noCarInTheDataBase_carModel)
    await callback_query.message.edit_reply_markup(GenerationOfInlineButtons(general_data.cars.models[dataAboutCar[callback_query.from_user.id]["carBrand"]], "Модели", page_number=dataAboutCar[callback_query.from_user.id]["page_numberModels"])[0])


async def handle_prev_button_model(callback_query: types.CallbackQuery):
    """
    Handle the previous button (car models) callback query

    This function handles the pagination for car models and updates the inline keyboard markup with the previous page.

    :param callback_query: The callback query
    :type callback_query: types.CallbackQuery
    """
    global dataAboutCar
    await callback_query.answer("")

    data = GenerationOfInlineButtons(general_data.cars.models[dataAboutCar[callback_query.from_user.id]["carBrand"]],
                                     "Модели", page_number=dataAboutCar[callback_query.from_user.id]["page_numberModels"] - 1)
    if data != -2:
        dataAboutCar[callback_query.from_user.id]["page_numberModels"] = data[1]
        await callback_query.message.edit_reply_markup(data[0])


async def handle_next_button_model(callback_query: types.CallbackQuery):
    """
    Handle the next button (car models) callback query

    This function handles the pagination for car models and updates the inline keyboard markup with the next page.

    :param callback_query: The callback query
    :type callback_query: types.CallbackQuery
    """
    global dataAboutCar
    await callback_query.answer("")

    data = GenerationOfInlineButtons(general_data.cars.models[dataAboutCar[callback_query.from_user.id]["carBrand"]],
                                     "Модели", page_number=dataAboutCar[callback_query.from_user.id]["page_numberModels"] + 1)
    if data != -2:
        dataAboutCar[callback_query.from_user.id]["page_numberModels"] = data[1]
        await callback_query.message.edit_reply_markup(data[0])


async def handle_model_button(callback_query: types.CallbackQuery):
    """
    Handle the model button callback query

    This function handles the selection of a car model and updates the carBrand in the dataAboutCar dictionary.
    It also sets the user state to get_dateAboutCarBrand and sends a message to select the car color.

    :param callback_query: The callback query
    :type callback_query: types.CallbackQuery
    """
    global dataAboutCar

    await callback_query.answer("")
    dataAboutCar[callback_query.from_user.id]["carBrand"] += f""" {
        callback_query.data}"""
    await RecordingInformationAboutCar.get_dateAboutCarBrand.set()
    colors = Colors()
    await bot.send_message(callback_query.from_user.id, text_3.t_carColour, reply_markup=colors.inline_keyboard_colors)


async def createDriver_dateAboutCarColour(callback_query: types.CallbackQuery):
    """
    Create driver & date about car colour

    This function handles the selection of the car color and updates the carColour in the dataAboutCar dictionary.
    It also sets the user state to get_dateAboutCarColour and sends a message to enter the car number.

    :param callback_query: The callback query
    :type callback_query: types.CallbackQuery
    """
    global dataAboutCar

    await callback_query.answer("")
    dataAboutCar[callback_query.from_user.id]["carColour"] = callback_query.data
    await RecordingInformationAboutCar.get_dateAboutCarColour.set()
    await bot.send_message(callback_query.from_user.id, text_3.t_carNumb)


async def createDriver_dateAboutCarNumbCar(message: types.Message):
    """
    Create driver & date about car & number car

    This function handles the entry of the car number and updates the carNumb in the dataAboutCar dictionary.
    It also sets the user state to check_data and sends a message to review the car information.

    :param message: The message containing the user's input
    :type message: types.Message
    """
    global dataAboutCar

    if len(message.text) > 4 and len(message.text) < 8:
        dataAboutCar[message.from_user.id]["carNumb"] = message.text
        await RecordingInformationAboutCar.check_data.set()
        await bot.send_message(message.from_user.id, f'{text_3.t_check_car}\n\nБренд: {dataAboutCar[message.from_user.id]["carBrand"]}\nЦвет: {dataAboutCar[message.from_user.id]["carColour"]}\nНомера: {dataAboutCar[message.from_user.id]["carNumb"]}\n\nЗаписать информацию о машине?', reply_markup=GeneralKeyboards.group_yesNo)
    else:
        # Foolproof
        await bot.send_message(message.from_user.id, text_1.t_foolproof_correct_data)


async def createDriver_dateAboutCar_check_car(message: types.Message):
    """
    Create driver & date about car & check car

    This function handles the confirmation of the car information by the user.
    If the user confirms, it sends a POST request to register the driver with the car information.
    If there are any errors or technical maintenance, it sends appropriate error messages.
    If the user does not confirm, it returns to the main menu.

    :param message: The message containing the user's input
    :type message: types.Message
    """
    global dataAboutUser, dataAboutTrip, dataAboutCar

    if message.text == "Да":
        try:
            # Send a POST request to delete the existing driver trip and register the driver with the car information
            userDataDelete = requests.post(f"{BASE_URL}/gettrips/drivers/delete", json={
                                           "user_id": f'{dataAboutUser[message.from_user.id]["user_id"]}'}).json()
            userData = requests.post(f"{BASE_URL}/registrations/drivers", json={
                "user_id": f'{dataAboutUser[message.from_user.id]["user_id"]}', "brand": f'{dataAboutCar[message.from_user.id]["carBrand"]}', "colour": f'{dataAboutCar[message.from_user.id]["carColour"]}', "numbcar": f'{dataAboutCar[message.from_user.id]["carNumb"]}'
            }).json()
        except Exception as e:
            log_error(e)
            userData = {"action": "technical maintenance"}

        if userData["action"] == "technical maintenance":
            # Send an error message and a technical maintenance message with a single button keyboard
            await bot.send_sticker(message.from_user.id, sticker=open("data/png/file_131068229.png", 'rb'))
            await bot.send_message(message.from_user.id, text_1.t_mistake)
            ts(1)
            await bot.send_message(message.from_user.id, text_2.t_technical_maintenance, reply_markup=GeneralKeyboards.single_btn_command_menu)
        else:
            data = inlineKeyboards.GenerationOfInlineButtons_calendar()
            await bot.send_message(message.from_user.id, text_3.t_ok_1)
            ts(1)
            await CreateTrip.get_dateAboutUser_carData.set()
            await bot.send_message(message.from_user.id, text_3.t_get_dateAbout_tripDates, reply_markup=data[2])
            dataAboutTrip[message.from_user.id]["page_number"] = [
                data[0], data[1], data[3], data[4]]

    elif message.text == "Нет":
        # Set the user state to start_state and send a message with the main menu
        await MenuUser.start_state.set()
        await bot.send_message(message.from_user.id, f'{text_1.t_welcome}', reply_markup=GeneralKeyboards.mainMenu)
    else:
        # If the input is not valid, send an error message with the yes/no keyboard
        # Foolproof
        await bot.send_message(message.from_user.id, text_1.t_foolproof_buttons, reply_markup=GeneralKeyboards.group_yesNo)
# _ _ _ End of driver registration _ _ _


async def handle_prev_button_date(callback_query: types.CallbackQuery):
    """
    Handle the previous button callback query

    This function handles the pagination for car brands and updates the inline keyboard markup with the previous page

    :param callback_query: The callback query
    :type callback_query: types.CallbackQuery
    """
    global dataAboutTrip
    page_number = dataAboutTrip[callback_query.from_user.id]["page_number"]

    await callback_query.answer("")
    data = GenerationOfInlineButtons_calendar(
        page_number[1] - 1, page_number[0], page_number[2] - 1, page_number[3])
    if data != -2:
        dataAboutTrip[callback_query.from_user.id]["page_number"] = [
            data[0], data[1], data[3], data[4]]
        await callback_query.message.edit_reply_markup(data[2])


async def handle_next_button_date(callback_query: types.CallbackQuery):
    """
    Handle the next button callback query

    This function handles the pagination for car brands and updates the inline keyboard markup with the next page

    :param callback_query: The callback query
    :type callback_query: types.CallbackQuery
    """
    global dataAboutTrip
    page_number = dataAboutTrip[callback_query.from_user.id]["page_number"]

    await callback_query.answer("")
    data = GenerationOfInlineButtons_calendar(
        page_number[1] + 1, page_number[0], page_number[2] + 1, page_number[3])
    if data != -2:
        dataAboutTrip[callback_query.from_user.id]["page_number"] = [
            data[0], data[1], data[3], data[4]]
        await callback_query.message.edit_reply_markup(data[2])


async def createTripForUser_tripDates_hours(callback_query: types.CallbackQuery):
    global dataAboutTrip

    if datetime.now() > datetime.strptime(callback_query.data, "%d.%m.%Y") + timedelta(days=1):
        await callback_query.answer("Выбери, пожалуйста, актуальную дату!", show_alert=True)
    else:
        dataAboutTrip[callback_query.from_user.id]["tripDates"] = remove_non_digits(
            callback_query.data)

        await callback_query.answer("")
        await CreateTrip.get_dateAbout_tripDates.set()
        # Check date
        if datetime.now().date() == datetime.strptime(callback_query.data, "%d.%m.%Y").date():
            dataAboutTrip[callback_query.from_user.id]["checkDate"] = 1
        else:
            dataAboutTrip[callback_query.from_user.id]["checkDate"] = 0
        await bot.send_message(callback_query.from_user.id, text_3.t_get_dateAbout_tripTimes, reply_markup=inlineKeyboards.GenerationOfInlineButtons_time())


async def createTripForUser_tripDates_minutes(callback_query: types.CallbackQuery):
    await CreateTrip.get_dateAbout_tripTimes_minutes.set()

    await callback_query.answer("")
    await callback_query.message.edit_reply_markup(inlineKeyboards.GenerationOfInlineButtons_time(typeOfTime="minutes", time_hours=callback_query.data))


async def createTripForUser_tripTimes(callback_query: types.CallbackQuery):
    """
    Create trip for user & time

    This function handles the entry of trip times by the user.
    It updates the tripTimes in the dataAboutTrip dictionary and sets the user state to get_dateAbout_tripPointA.
    It also sends a message to select the trip starting point (campus).

    :param message: The message containing the user's input
    :type message: types.Message
    """
    global dataAboutTrip

    if dataAboutTrip[callback_query.from_user.id]["checkDate"] == 1 and datetime.now().time() > datetime.strptime(callback_query.data, "%H:%M").time():

        await CreateTrip.get_dateAbout_tripDates.set()
        await bot.send_message(callback_query.from_user.id, text_3.t_get_dateAbout_tripTimes, reply_markup=inlineKeyboards.GenerationOfInlineButtons_time())
        await callback_query.answer("Выбери, пожалуйста, актуальное время!", show_alert=True)
    else:
        dataAboutTrip[callback_query.from_user.id]["tripTimes"] = remove_non_digits(
            callback_query.data)

        await CreateTripPassenger.set_direction.set()
        await bot.send_message(callback_query.from_user.id, text_3.t_get_dateAbout_tripRoute, reply_markup=direction_keyboard())


async def createTripForUser_check(message: types.Message):
    """
    Send data to database

    This function handles the confirmation of trip details by the user.
    If the user confirms, it sends a POST request to create the trip in the database.
    It also checks for suitable trips and sends appropriate messages based on the type of member.

    :param message: The message containing the user's input
    :type message: types.Message
    """
    global dataAboutUser, dataAboutTrip, dataAboutCar
    if message.text == "Да":
        try:
            userData = requests.post(f"{BASE_URL}/сreatingtrips",
                                     json={
                "user_id": f'{dataAboutUser[message.from_user.id]["user_id"]}',
                "typeofmembers": f'{dataAboutTrip[message.from_user.id]["typeOfMembers"]}',
                "tripsdates": f'{dataAboutTrip[message.from_user.id]["tripDates"]}',
                "tripstimes": f'{dataAboutTrip[message.from_user.id]["tripTimes"]}',
                "direction_name": f'{dataAboutTrip[message.from_user.id]["directionName"]}',
                "route_number": dataAboutTrip[message.from_user.id]["routeNumber"],
                "pointa": dataAboutTrip[message.from_user.id]["pointA"],
                "pointb": dataAboutTrip[message.from_user.id]["pointB"],
                "number_of_passengers": 0,
                "status": "waiting",
                "maximum_number_of_passengers": dataAboutTrip[message.from_user.id]["tripNumberOfPassengers"]
            }).json()
            # Processing data from the database "AgreedTrips"
            userDataAgreedTrips = requests.post(
                f"{BASE_URL}/gettrips/agreedTrips/suitableTrips", json={"id": "test"}).json()
            userDataAgreedTrips["data"] = remove_dicts_with_id(
                userDataAgreedTrips["data"], dataAboutUser[message.from_user.id]["user_id"], "id_driver")
            # Processing data from the database "Trips"
            userDataTrips = requests.post(
                f"{BASE_URL}/gettrips/trips/suitableTrips", json={"id": "test"}).json()
            userData1 = remove_dicts_with_id(
                userDataTrips["data"], dataAboutUser[message.from_user.id]["user_id"], "id")
            dataAboutTrip[message.from_user.id]["id_trip"] = userData["id_trip"]

            if dataAboutTrip[message.from_user.id]["typeOfMembers"] == "driver":
                dataAboutTrip[message.from_user.id]["id_agreedTrips"] = userData["id_agreedTrips"]
        except Exception as e:
            log_error(e)
            userData = {"action": "technical maintenance"}

        if userData["action"] == "technical maintenance":
            await bot.send_sticker(message.from_user.id, sticker=open("data/png/file_131068229.png", 'rb'))
            await bot.send_message(message.from_user.id, text_1.t_mistake)
            ts(1)
            await bot.send_message(message.from_user.id, text_2.t_technical_maintenance, reply_markup=GeneralKeyboards.single_btn_command_menu)

        else:
            await bot.send_message(message.from_user.id, text_3.t_ok)

            # if user a driver
            if dataAboutTrip[message.from_user.id]["typeOfMembers"] == "driver":
                # Processing data from the database
                userDataPassengers = remove_dicts_with_id(
                    userData1, "driver", "typeofmembers")
                userDataPassengers_filter_trip_list = filter_trip_list(
                    userDataPassengers, dataAboutTrip[message.from_user.id]["pointA"], dataAboutTrip[message.from_user.id]["pointB"])
                userData2 = create_new_dict(
                    userDataPassengers_filter_trip_list)
                userData2[dataAboutTrip[message.from_user.id]["id_agreedTrips"]] = [
                    dataAboutTrip[message.from_user.id]["tripDates"], dataAboutTrip[message.from_user.id]["tripTimes"]]
                suitableTripIDs = algorithmForCalculatingSuitableTripsTime(userData2, dataAboutTrip[message.from_user.id]["id_agreedTrips"], algorithmForCalculatingSuitableTripsDate(
                    userData2, dataAboutTrip[message.from_user.id]["id_agreedTrips"]), 60)

                if len(suitableTripIDs) == 0:
                    await bot.send_message(message.from_user.id, text_3.t_no_matches, reply_markup=GeneralKeyboards.single_btn_command_menu)

                else:
                    check = 0
                    for i in suitableTripIDs:
                        if i == dataAboutTrip[message.from_user.id]["id_trip"]:
                            continue
                        try:
                            new_lst = [dict for dict in userDataPassengers if dict.get(
                                "id_trip") == i][0]
                            dateRequest = requests.post(f"{BASE_URL}/settrips/agreedTrips", json={
                                                        "id_passenger": new_lst["id"], "id_trip": i, "id_agreed_trip": dataAboutTrip[message.from_user.id]["id_agreedTrips"]}).json()
                        except Exception as e:
                            log_error(e)
                            await bot.send_sticker(message.from_user.id, sticker=open("data/png/file_131068229.png", 'rb'))
                            await bot.send_message(message.from_user.id, text_1.t_mistake)
                            ts(1)
                            await bot.send_message(message.from_user.id, text_2.t_technical_maintenance, reply_markup=GeneralKeyboards.single_btn_command_menu)

                        else:
                            if dateRequest["action"] == "success" and dateRequest["status"] == "success":
                                try:
                                    agreedUserData = dateRequest = requests.post(
                                        f"{BASE_URL}/getusers", json={"id": new_lst["id"]}).json()["data"]
                                except Exception as e:
                                    log_error(e)
                                    break
                                user = await bot.get_chat(chat_id=agreedUserData["id_tg"])
                                try:
                                    dateRequestDriver = requests.post(f"{BASE_URL}/gettrips/drivers", json={
                                                                      "user_id": dataAboutUser[message.from_user.id]["user_id"]}).json()["data"][0]
                                except Exception as e:
                                    log_error(e)
                                    await bot.send_sticker(message.from_user.id, sticker=open("data/png/file_131068229.png", 'rb'))
                                    await bot.send_message(message.from_user.id, text_1.t_mistake)
                                    ts(1)
                                    await bot.send_message(message.from_user.id, text_2.t_technical_maintenance, reply_markup=GeneralKeyboards.single_btn_command_menu)
                                # Notification to the driver
                                await bot.send_sticker(message.from_user.id, sticker=open("data/png/file_131068230.png", 'rb'))
                                await bot.send_message(message.from_user.id, text_3.t_good_1)
                                ts(1)
                                await bot.send_message(message.from_user.id, text_3.t_good_2)
                                await bot.send_message(message.from_user.id, f'Имя: {agreedUserData["name"]}\ntg: @{user.username}',  reply_markup=GeneralKeyboards.single_btn_command_menu)
                                await bot.send_message(agreedUserData["id_tg"], text_3.t_good_1)
                                # Notification to the passenger
                                await bot.send_sticker(agreedUserData["id_tg"], sticker=open("data/png/file_131068230.png", 'rb'))
                                await bot.send_message(agreedUserData["id_tg"], text_3.t_good_2)
                                await bot.send_message(agreedUserData["id_tg"], f'''Имя: {dataAboutUser[message.from_user.id]["user_name"]}\ntg: @{message.from_user.username}\nДата:
                                                       {format_date_time(dataAboutTrip[message.from_user.id]["tripDates"])}\nВремя:
                                                       {format_date_time(dataAboutTrip[message.from_user.id]["tripTimes"])}\nБренд машины:
                                                       {dateRequestDriver["brand"]}\nЦвет машины: {dateRequestDriver["colour"]}\nНомера машины: {dateRequestDriver["numbcar"]}''',
                                                       reply_markup=GeneralKeyboards.single_btn_command_menu)
                                check = 1
                                break
                    if check == 0:
                        await bot.send_message(message.from_user.id, text_3.t_no_matches, reply_markup=GeneralKeyboards.single_btn_command_menu)

            # if user a passenger
            elif dataAboutTrip[message.from_user.id]["typeOfMembers"] == "passenger":
                # Processing data from the database
                userDataAgreedTrips["data"] = filter_trip_list(
                    userDataAgreedTrips["data"], dataAboutTrip[message.from_user.id]["pointA"], dataAboutTrip[message.from_user.id]["pointB"])
                userData2 = create_new_dict(userDataAgreedTrips["data"])
                userData2[dataAboutTrip[message.from_user.id]["id_trip"]] = [
                    dataAboutTrip[message.from_user.id]["tripDates"], dataAboutTrip[message.from_user.id]["tripTimes"]]
                suitableTripIDs = algorithmForCalculatingSuitableTripsTime(userData2, dataAboutTrip[message.from_user.id]["id_trip"], algorithmForCalculatingSuitableTripsDate(
                    userData2, dataAboutTrip[message.from_user.id]["id_trip"]), 60)

                if len(suitableTripIDs) == 0:
                    await bot.send_message(message.from_user.id, text_3.t_no_matches, reply_markup=GeneralKeyboards.single_btn_command_menu)
                else:
                    check = 0
                    for i in suitableTripIDs:
                        try:
                            dateRequest = requests.post(f"{BASE_URL}/settrips/agreedTrips", json={
                                                        "id_passenger": dataAboutUser[message.from_user.id]["user_id"], "id_trip": dataAboutTrip[message.from_user.id]["id_trip"],
                                                        "id_agreed_trip": i}).json()
                        except Exception as e:
                            log_error(e)
                            await MenuUser.start_state.set()
                            await bot.send_sticker(message.from_user.id, sticker=open("data/png/file_131068229.png", 'rb'))
                            await bot.send_message(message.from_user.id, text_1.t_mistake)
                            ts(1)
                            await bot.send_message(message.from_user.id, text_2.t_technical_maintenance, reply_markup=GeneralKeyboards.single_btn_command_menu)

                        else:
                            if dateRequest["action"] == "success" and dateRequest["status"] == "success":
                                driver_id = next(
                                    (
                                        trip.get("id_driver")
                                        for trip in userDataAgreedTrips["data"]
                                        if trip.get("id_trip") == i
                                    ),
                                    None,
                                )
                                try:
                                    agreedUserData = requests.post(
                                        f"{BASE_URL}/getusers", json={"id": driver_id}).json()
                                except Exception as e:
                                    log_error(e)
                                    await bot.send_sticker(message.from_user.id, sticker=open("data/png/file_131068229.png", 'rb'))
                                    await bot.send_message(message.from_user.id, text_1.t_mistake)
                                    ts(1)
                                    await bot.send_message(message.from_user.id, text_2.t_technical_maintenance, reply_markup=GeneralKeyboards.single_btn_command_menu)
                                else:
                                    if agreedUserData["action"] == "errorData":
                                        break
                                    else:
                                        agreedUserData = agreedUserData["data"]
                                try:
                                    dateRequestDriver = requests.post(
                                        f"{BASE_URL}/gettrips/drivers", json={"user_id": driver_id}).json()["data"][0]
                                except Exception as e:
                                    log_error(e)
                                    await MenuUser.start_state.set()
                                    await bot.send_sticker(message.from_user.id, sticker=open("data/png/file_131068229.png", 'rb'))
                                    await bot.send_message(message.from_user.id, text_1.t_mistake)
                                    ts(1)
                                    await bot.send_message(message.from_user.id, text_2.t_technical_maintenance, reply_markup=GeneralKeyboards.single_btn_command_menu)
                                # Notification to the passenger
                                await bot.send_sticker(message.from_user.id, sticker=open("data/png/file_131068230.png", 'rb'))
                                await bot.send_message(message.from_user.id, text_3.t_good_1)
                                ts(1)
                                await bot.send_message(message.from_user.id, text_3.t_good_2, reply_markup=GeneralKeyboards.single_btn_command_menu)
                                user = await bot.get_chat(chat_id=agreedUserData["id_tg"])
                                await bot.send_message(message.from_user.id, f'''Имя: {agreedUserData["name"]}\ntg: @{user.username}\nБренд машины:
                                                       {dateRequestDriver["brand"]}\nЦвет машины: {dateRequestDriver["colour"]}\nНомера машины: {dateRequestDriver["numbcar"]}''',
                                                       reply_markup=GeneralKeyboards.single_btn_command_menu)
                                # Notification to the driver
                                await bot.send_sticker(agreedUserData["id_tg"], sticker=open("data/png/file_131068230.png", 'rb'))
                                await bot.send_message(agreedUserData["id_tg"], text_3.t_good_1)
                                ts(1)
                                await bot.send_message(agreedUserData["id_tg"], text_3.t_good_2, reply_markup=GeneralKeyboards.single_btn_command_menu)
                                await bot.send_message(agreedUserData["id_tg"], f'''Имя: {dataAboutUser[message.from_user.id]["user_name"]}\ntg: @{message.from_user.username}\nДата:
                                                       {format_date_time(dataAboutTrip[message.from_user.id]["tripDates"])}\nВремя:
                                                       {format_date_time(dataAboutTrip[message.from_user.id]["tripTimes"])}''', reply_markup=GeneralKeyboards.single_btn_command_menu)
                                check = 1
                                break
                    if check == 0:
                        await bot.send_message(message.from_user.id, text_3.t_no_matches, reply_markup=GeneralKeyboards.single_btn_command_menu)
    else:
        await bot.send_message(message.from_user.id, text_1.t_time, reply_markup=GeneralKeyboards.single_btn_command_menu)


# _ _ _ Admin _ _ _

RegisteredUsers = ["730611481", "1380181607"]


class RegisteredUser(StatesGroup):
    """Register state"""
    Register = State()


async def start(message: types.Message):
    """Checks by tg id"""
    check = sum(int(i) == int(message.from_user.id) for i in RegisteredUsers)
    if check == 0:
        await bot.send_message(message.from_user.id, """ru: У вас нет доступа к функционалу бота, свяжитесь с @muslims_elhamdulillah\n
en: You don't have access to the bot functionality, contact @muslims_elhamdulillah""")
    else:
        await RegisteredUser.Register.set()
        await bot.send_message(message.from_user.id, "ru: Введите Telegram ID\n\nen: Enter the Telegram ID")


async def get_user_info(message: types.Message):
    """Transmits account information by telegram id"""
    try:
        user = await bot.get_chat(chat_id=message.text)
        await bot.send_message(message.from_user.id,
                               f"""ID: {message.text}
Username: @{user.username}
First Name: {user.first_name}
Last Name: {user.last_name}
""")
    except Exception as e:
        await bot.send_message(message.from_user.id, "ru: Ошибка введенного Telegram ID \n\nen: Error in the Telegram ID entered")


async def get_all_users(message: types.Message):
    '''Получение всех пользователей'''

    dateRequest = requests.get(f"{BASE_URL}/admin/getAllColumns/users", json={}).json()

    users_data = dateRequest.get('data', [])

    chunk_size = 10  # Максимальное количество элементов в одном сообщении
    chunks = [users_data[i:i + chunk_size] for i in range(0, len(users_data), chunk_size)]
    check = 0

    for chunk in chunks:
        if check == 2:
            break
        users_message = "\n".join([
            f"ID: {users['id']}\n"
            f"Имя: {users['name']}\n"
            f"Номер телефона: {users['numb']}\n"
            f"ID TG: {users['id_tg']}\n"
            f"Фамилия: {users['surname']}\n"
            for users in chunk
        ])
        check += 1
        await bot.send_message(message.from_user.id, users_message, reply_markup=GeneralKeyboards.mainMenu)


# _ _ _ The function of a joint trip _ _ _


async def trip_cancellation_button(callback_query: types.CallbackQuery):
    """
    Handle the title button callback query

    This function sends message

    :param callback_query: The callback query
    :type callback_query: types.CallbackQuery
    """
    await callback_query.answer("Поиск попутчиков приостановлен")


async def get_information_about_fellow_travelers(callback_query: types.CallbackQuery):
    """
    Handle the title button callback query

    This function sends message

    :param callback_query: The callback query
    :type callback_query: types.CallbackQuery
    """
    try:
        dateRequest1: dict
        dateRequest1 = requests.post(
            f"{BASE_URL}/checkuser", json={"id_tg": callback_query.from_user.id}).json()
    except Exception as e:
        log_error(e)
        dateRequest1 = {"action": "technical maintenance"}
    if dateRequest1 != {"action": "technical maintenance"}:
        trips_id = callback_query.data
        data = trips_id.replace('[', '').replace(
            ']', '').replace('\'', '').replace(' ', '')
        result = data.split(',')
        try:
            dateRequest2: dict
            dateRequest2 = requests.post(
                f"{BASE_URL}/gettrips/trips/Trips", json="").json()["data"]
        except Exception as e:
            log_error(e)
            dateRequest2 = {"action": "technical maintenance"}
        if dateRequest2 != {"action": "technical maintenance"}:
            for i in result:
                try:
                    result_id = [d['id']
                                 for d in dateRequest2 if d['id_trip'] == i][0]
                    result_date = format_date_time(
                        [d['tripsdates'] for d in dateRequest2 if d['id_trip'] == i][0])
                    result_time = format_date_time(
                        [d['tripstimes'] for d in dateRequest2 if d['id_trip'] == i][0])
                except:
                    pass

                try:
                    dateRequest_user: dict
                    dateRequest_user = requests.post(
                        f"{BASE_URL}/getusers", json={"id": f'{result_id}'}).json()["data"]
                except Exception as e:
                    log_error(e)
                    dateRequest_user = {"action": f"technical maintenance {e}"}
                if dateRequest_user != {"action": "technical maintenance"}:
                    result_id_tg = dateRequest_user["id_tg"]
                    user = await bot.get_chat(chat_id=result_id_tg)
                    result_user_name = dateRequest_user["name"]
                    await bot.send_message(callback_query.from_user.id, f'Имя: {result_user_name}\ntg: @{user.username}\nДата: {result_date}\nВремя: {result_time}')

        else:
            await callback_query.answer("Возникла ошибка")
    else:
        await callback_query.answer("Возникла ошибка")


async def top_up_handle_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Handle the replenishment buttons callback query

    This function handles the accept and reject balance replenishment buttons

    :param callback_query: The callback query
    :type callback_query: types.CallbackQuery
    :param state: For the possibility of further upgrade of the bot
    :type state: FSMContext
    """
    global amount, dataAboutUser
    action = callback_query.data



    if 'top_up_rubles_' in action:
        amount = float(action.replace('top_up_rubles_', ''))
        await bot.answer_callback_query(callback_query.id)
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, f'Подтвердите пополнение\n\nСумма пополнения: {amount} ₽',
                               reply_markup=SimpleKeyboardsForReplenishBalance.confirm_cancel_inline_kb)


    if action == 'confirmation_of_replenishment_of_the_balance':

        # sending request to the server to update db
        try:
            balance_response = requests.post(f"{BASE_URL}/balance/recharging", json={"user_id": dataAboutUser[callback_query.from_user.id]["user_id"], "credit": amount}).json()
            if balance_response["action"] == "success":
                await bot.answer_callback_query(callback_query.id)
                await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
                await bot.send_message(callback_query.from_user.id, f'Пополнение подтверждено! +{amount} ₽',
                                       reply_markup=GeneralKeyboards.mainMenu)
                await MenuUser.start_state.set()
            else:
                raise ValueError(balance_response)
        except Exception as e:
            await bot.answer_callback_query(callback_query.id)
            await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
            await bot.send_message(callback_query.from_user.id, 'Ошибка!', reply_markup=GeneralKeyboards.mainMenu)
            await MenuUser.start_state.set()
            log_error(e)



    if action == 'canceling_of_replenishment_of_the_balance':
        await bot.answer_callback_query(callback_query.id)
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, 'Пополнение отменено!',
                               reply_markup=GeneralKeyboards.mainMenu)
        await MenuUser.start_state.set()



# _ _ _ Packing the registration of handlers into functions by groups _ _ _


def startReg(dp=dp):
    dp.register_message_handler(startCommand, commands=["start"], state="*")
    dp.register_message_handler(startCommand, commands=["menu"], state="*")
    dp.register_message_handler(startCommand, commands=["start"])
    dp.register_message_handler(startCommand, commands=["menu"])
    dp.register_message_handler(getTripsByDirection, commands=["getTripsByDirection"], state="*")
    dp.register_message_handler(getDrivers, commands=["getDrivers"], state="*")
    dp.register_message_handler(user_agreement, state=AgreementUser.get_user_info)

    dp.register_message_handler(mainMenu)
    dp.register_callback_query_handler(
        trip_cancellation_button, text="cancel a trip", state="*")
    dp.register_callback_query_handler(
        handle_cancel_button, text="cancel", state="*")
    dp.register_callback_query_handler(
        handle_title_button, text="title", state="*")
    dp.register_message_handler(startRegister, state=UserState.start_register)
    dp.register_message_handler(
        first_register_name, state=UserState.get_dateAboutUser_name)
    dp.register_message_handler(
        first_register_surname, state=UserState.get_dateAboutUser_surname)
    dp.register_message_handler(
            first_register_number, state=UserState.get_dateAboutUser_number, content_types=types.ContentType.CONTACT)
    dp.register_message_handler(
        first_register_number, state=UserState.get_dateAboutUser_number)


def trips(dp=dp):
    dp.register_message_handler(
        createTripForUser_typeOfMembers, state=CreateTrip.start_creating)
    dp.register_message_handler(
        createTripForUser_carData, state=CreateTrip.get_dateAboutUser_typeOfMembers)
    dp.register_message_handler(
        createTripForUser_tripNumberOfPassengers, state=CreateTrip.get_tripNumberOfPassengers)
    dp.register_callback_query_handler(
        handle_prev_button_date, text="prev", state=CreateTrip.get_dateAboutUser_carData)
    dp.register_callback_query_handler(
        handle_next_button_date, text="next", state=CreateTrip.get_dateAboutUser_carData)
    dp.register_callback_query_handler(
        createTripForUser_tripDates_hours, state=CreateTrip.get_dateAboutUser_carData)
    dp.register_callback_query_handler(
        createTripForUser_tripDates_minutes, state=CreateTrip.get_dateAbout_tripDates)
    dp.register_callback_query_handler(
        createTripForUser_tripTimes, state=CreateTrip.get_dateAbout_tripTimes_minutes)

    dp.register_message_handler(
        createTripForUser_check, state=CreateTripPassenger.set_confirmation)


def car(dp=dp):
    dp.register_callback_query_handler(
        handle_prev_button, text="prev", state=RecordingInformationAboutCar.start_state)
    dp.register_callback_query_handler(
        handle_next_button, text="next", state=RecordingInformationAboutCar.start_state)
    dp.register_callback_query_handler(
        handle_prev_button_model, text="prev", state=RecordingInformationAboutCar.start_state_model)
    dp.register_callback_query_handler(
        handle_next_button_model, text="next", state=RecordingInformationAboutCar.start_state_model)
    dp.register_callback_query_handler(
        handle_brand_button, state=RecordingInformationAboutCar.start_state)
    dp.register_callback_query_handler(
        handle_model_button, state=RecordingInformationAboutCar.start_state_model)
    dp.register_callback_query_handler(
        createDriver_dateAboutCarColour, state=RecordingInformationAboutCar.get_dateAboutCarBrand)
    dp.register_message_handler(createDriver_dateAboutCarNumbCar,
                                state=RecordingInformationAboutCar.get_dateAboutCarColour)
    dp.register_message_handler(
        createDriver_dateAboutCar_check_car, state=RecordingInformationAboutCar.check_data)
    dp.register_message_handler(functionFoolproof, state=[RecordingInformationAboutCar.start_state,
                                                          RecordingInformationAboutCar.start_state_model,
                                                          RecordingInformationAboutCar.get_dateAboutCarBrand,
                                                          CreateTrip.get_dateAbout_tripTimes_minutes,
                                                          CreateTrip.get_dateAbout_tripDates,
                                                          CreateTrip.get_dateAboutUser_carData])  # Foolproof


def menuAll(dp=dp):
    dp.register_message_handler(aboutCommand, state=MenuAbout.start_state)
    dp.register_message_handler(mainMenu, state=MenuUser.start_state)
    dp.register_message_handler(
        aboutCommandRegistered, state=MenuUser.go_to_about)
    dp.register_message_handler(
        myProfileCommandRegistered, state=MenuUser.set_profileInfo)
    dp.register_message_handler(
        myTripsCommandRegistered, state=MenuUser.set_myTrips)
    dp.register_callback_query_handler(top_up_handle_callback, state=ProfileMenu.set_top_up_balance)
    dp.register_message_handler(check_my_trips, state=CheckTripsMenu.start_state)
    dp.register_message_handler(become_driver_end, state=BecomeDriver.start_become_dr)  # become driver

    dp.register_message_handler(leave_review, state=LeaveReview.start_state)
    dp.register_message_handler(leave_review_confirmation, state=LeaveReview.set_confirmation)

    dp.register_callback_query_handler(choose_direction, state=CreateTripPassenger.set_direction)
    dp.register_callback_query_handler(choose_route, state=CreateTripPassenger.set_route)
    dp.register_callback_query_handler(createTrip_pointA, state=CreateTripPassenger.set_pointA)
    dp.register_callback_query_handler(createTrip_pointB, state=CreateTripPassenger.set_pointB)

    dp.register_callback_query_handler(choose_direction_for_search, state=GetTrips.get_trips_by_direction)


def adminCommands(dp=dp):
    dp.register_message_handler(start, commands="admin", state="*")
    dp.register_message_handler(get_user_info, state=RegisteredUser.Register)
    # dp.register_callback_query_handler(get_information_about_fellow_travelers, state="*")
    dp.register_message_handler(get_all_users, commands="users", state="*")
