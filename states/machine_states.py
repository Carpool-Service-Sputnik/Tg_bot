"""
Classes with state machines:
- States group for the registration process
- States group for the process of creating a trip
- States group for recording information about the car
- States group for the menu status
- States group for the about menu status

Example usage:

menu_about_state = MenuAbout()
menu_about_state.start_state.set()

def menuAll(dp=dp):
    dp.register_message_handler(startCommand, commands=["menu"], state="*")
    dp.register_message_handler(aboutCommand, state=MenuAbout.start_state)
"""


from aiogram.dispatcher.filters.state import State, StatesGroup




class UserState(StatesGroup):
    """Register state"""
    start_register = State()
    get_dateAboutUser_name = State()
    get_dateAboutUser_surname = State()
    get_dateAboutUser_number = State()
    get_dateAboutUser_location = State()
    go_menu = State()


class CreateTrip(StatesGroup):
    """Creating a trip state"""
    start_creating = State()
    get_dateAboutUser_typeOfMembers = State()
    get_dateAboutUser_carData = State()
    get_tripNumberOfPassengers = State()
    get_dateAbout_tripDates = State()
    get_dateAbout_tripTimes = State()
    get_dateAbout_tripTimes_minutes = State()
    get_dateAbout_tripPointA = State()
    get_dateAbout_tripPointB = State()
    check_data = State()


class RecordingInformationAboutCar(StatesGroup):
    """Recording information about the car"""

    start_state = State()
    start_state_model = State()
    get_dateAboutCarBrand = State()
    get_dateAboutCarColour = State()
    get_dateAboutCarNumbCar = State()
    check_data = State()


class MenuUser(StatesGroup):
    """Menu status"""
    start_state = State()
    set_profileInfo = State()
    set_myTrips = State()
    go_to_about = State()


class MenuAbout(StatesGroup):
    """Menu about status"""
    start_state = State()
    set_FAQ = State()
    set_about = State()
    set_instruction = State()
