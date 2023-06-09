from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def get_num_from_usr():
    return ReplyKeyboardMarkup().add(
        KeyboardButton(
            text="Поделиться",
            request_contact=True
        )
    )


def on_start_keyboard():
    keyboard = ReplyKeyboardMarkup()
    keyboard.add(
        *[
            KeyboardButton(txt) for txt in ("Повредил груз", "Авария", "Полиция",
                                            "Техническая помощь", "Бухгалтерия", "Мои документы",
                                            "Топливная карта")
        ]
    )
    keyboard.add(
        *[KeyboardButton(txt) for txt in ("Страховкa", "Приемка трака/трейлера", "Отдел аренды", "Дpyгoe")]
    )
    return keyboard


def technical_support_keyboard():
    return ReplyKeyboardMarkup().add(
        *[KeyboardButton(txt) for txt in ("Назад", "Запись на ТО", "Проблемы с машиной")]
    )


def buchaltery_keyboard():
    return ReplyKeyboardMarkup().add(
        *[KeyboardButton(txt) for txt in ("Не получил деньги!", "Как и когда происходит оплата", "Ошибка в чеке",
                                          "Депозирование чека", "Реквизиты компании", "Виды оплат за лоад",
                                          "Отправить фотографию чека", "Другое.", "Назад")]
    )


def buch_yes_no():
    return ReplyKeyboardMarkup().add(
        KeyboardButton(text="Да"),
        KeyboardButton(text="Нет")
    )


def my_documents_keyboard():
    return ReplyKeyboardMarkup().add(
        *[KeyboardButton(txt) for txt in ("Страховка COI", "Lease Agreement (контракт)", "Signs",
                                          "Необходимые в рейс документы", "Медицинский сертификат", "Назад")]
    )


def fuel_card_start():
    return ReplyKeyboardMarkup().add(
        *[KeyboardButton(txt) for txt in ["Работа с топливной картой", "Вас интересует как пользоваться топливной картой",
                                          "Не проходит транзакция", "Отклоняет оплату", "Другoе ", "Назад"]]
    )


def how_to_work_with_fuel_card():
    return ReplyKeyboardMarkup().add(
        *[KeyboardButton(txt) for txt in ["Схемы работы по топливным картам", "Виртуальные топливные карты",
                                          "Получить номер топливной карты", "Пластиковые топливные карты", "Назад"]]
    )


def virtual_fuel_cards_keyboard():
    return ReplyKeyboardMarkup().add(
        *[KeyboardButton(txt) for txt in ["Получить номер топливной карты", "Назад"]]
    )


def plastic_fuel_cards_keyboard():
    return ReplyKeyboardMarkup().add(
        *[KeyboardButton(txt) for txt in ["Заказать на почту на выбранный адрес компании", "Забрать в офисе компании",
                                          "Назад"]]
    )


def insurance_start_keyboard():
    return ReplyKeyboardMarkup().add(
        *[KeyboardButton(txt) for txt in ["Cтрахoвкa", "Сумма страховки не соответствует ранее заявленной",
                                          "Страховой случай", "Другоe", "Назад"]]
    )


def tracks():
    return ReplyKeyboardMarkup().add(
        *[KeyboardButton(txt) for txt in ["Трак", "Трейлер", "Назад"]]
    )


def rent_keyboard():
    return ReplyKeyboardMarkup().add(
        *[KeyboardButton(txt) for txt in ["Машина", "Прицеп", "Назад"]]
    )


def back():
    return ReplyKeyboardMarkup().add(KeyboardButton("Назад"))

