from aiogram.dispatcher.filters.state import State, StatesGroup


class StartStateGetNumber(StatesGroup): GET_NUMBER = State()


class CargoHaveBeenDamaged(StatesGroup):
    WAITING_FOR_PHOTO = State()
    SITUATION_DESCRIPTION = State()


class Accident(StatesGroup): ACCIDENT_CONTEXT = State()


class TechnicalSupport(StatesGroup):
    ASK_FOR_TO = State()
    CAR_HAS_BEEN_BROKEN = State()
    GET_BROKE_PHOTO = State()


class BuchalteryStates(StatesGroup):
    MAIN_STATE = State()
    GET_INFO4 = State()
    YES_NO_QUESTION_STATE = State()
    GET_TICKET_PHOTO = State()
    DONT_UNDERSTAND = State()


class DocumentsStates(StatesGroup): HANDLE_3FUNCTIONS_IN_ONE = State()


class FuelCardsStates(StatesGroup):
    YES_NO_QUESTION = State()
    NO_PROBLEM_TRANSACTION = State()
    OTHER_FUEL = State()


class Insurance(StatesGroup):
    GET_DATA = State()


class Tracks(StatesGroup):
    TRACK_STATE = State()


class RentState(StatesGroup):
    COLLECT_INFO = State()


class MainOtherState(StatesGroup):
    OTHER_PUBLIC_STATE = State()
