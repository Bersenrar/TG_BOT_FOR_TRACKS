# Aiogram Imports
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor, callback_data
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Importing regular expressions
import re

# Iternal config Import
from config import BOT_TOKEN

# Iternal keyaboards Import
from keyboards import on_start_keyboard, technical_support_keyboard, buchaltery_keyboard, buch_yes_no, back,\
    my_documents_keyboard, fuel_card_start, how_to_work_with_fuel_card, virtual_fuel_cards_keyboard, \
    plastic_fuel_cards_keyboard, insurance_start_keyboard, tracks, rent_keyboard, get_num_from_usr

# Iternal states Import
from states import StartStateGetNumber, CargoHaveBeenDamaged, Accident, TechnicalSupport, BuchalteryStates, \
    DocumentsStates, FuelCardsStates, Insurance, Tracks, RentState, MainOtherState

# Iternal Logger Import
import logging


#Iternal Re Imports

from re_patterns import *


bot = Bot(BOT_TOKEN)

storage = MemoryStorage()

dp = Dispatcher(bot=bot, storage=storage)
logger = logging.getLogger("BOT_LOGS")

USER_KEYBOARDS = []


# TODO-----------------------Люблю Шимпанзе---------------------------
def if_user_crazy_monkey_check(massive_words, user_input):
    if user_input in massive_words:
        return True
    return False


# TODO-----------------------Стартовое сообщение---------------------------


@dp.message_handler(commands=["start"])
async def on_start(message:types.Message):
    '''
    Функция реагирующая на команду /start
    запрашивает номер телефона пользователя
    :param message:
    :return:
    '''
    await message.answer(text="Добрый день поделитесь вашим номером телефона", reply_markup=get_num_from_usr())
    await StartStateGetNumber.GET_NUMBER.set()


@dp.message_handler(state=StartStateGetNumber.GET_NUMBER, content_types=types.ContentTypes.CONTACT)
async def on_start_get_number(contact:types.contact, state:FSMContext):
    '''
    Стартовая функция для получения номера телефона если номер был введён в неверном формате вызывается функция
    on_start
    :param message: Обьект представляющий сообщение пользователя
    :param state:
    :return:
    '''
    # check = re.findall(r"(\+?380)?(0?\d{9})", message.text)

    # def validate_phone_number(phone_number):
    #     pattern = r'^\+?38(\d{10})$'
    #     return re.match(pattern, phone_number) is not None

    # if validate_phone_number(message.text):
        # USER_KEYBOARDS.append(on_start_keyboard())
    await contact.answer(text="Вас приветствует команда поддержки, здравствуйте! Что у вас произошло?",
                         reply_markup=on_start_keyboard())
    # await state.update_data(phone_number=contact.phone_number)
    await state.reset_state(with_data=False)
    # else:
    #     await on_start(message)

# TODO-----------------------Повредил Груз---------------------------


@dp.message_handler(lambda msg: msg.text == "Повредил груз")
async def cargo_damaged(message:types.Message, state:FSMContext):
    await message.answer(text="Приложите фото", reply_markup=back())
    await CargoHaveBeenDamaged.WAITING_FOR_PHOTO.set()


@dp.message_handler(state=CargoHaveBeenDamaged.WAITING_FOR_PHOTO, content_types=types.ContentTypes.PHOTO)
async def getting_damaged_cargo_photo(message:types.Message, state:FSMContext):
    ''''''
    # photos = [await bot.download_file_by_id(id_p.file_id) for id_p in message.photo]
    await state.update_data(
        damage_car_photo = await bot.download_file_by_id(message.photo.pop().file_id)
    )
    await state.reset_state(with_data=False)
    await message.answer(text="Опишите, что произошло")
    await CargoHaveBeenDamaged.SITUATION_DESCRIPTION.set()


@dp.message_handler(state=CargoHaveBeenDamaged.SITUATION_DESCRIPTION)
async def damaged_context(message:types.Message, state:FSMContext):
    if message.text == "Назад":
        await state.reset_state(with_data=False)
        await message.answer(text="Отмена действия", reply_markup=on_start_keyboard())
    else:
        await state.update_data(
            damaged_situation_description = message.text
        )
        await message.answer(
            text="Ваша заявка принята. В скором времени к вам подключится оператор для решения вашей проблемы.",
            reply_markup=on_start_keyboard()
        )
        # Пункт 4
        await result(message=message, state=state, situation_type="CARGO_DAMAGED")


@dp.message_handler(state=CargoHaveBeenDamaged.WAITING_FOR_PHOTO, content_types=types.ContentTypes.ANY)
async def getting_damaged_cargo_photo_but_user_is_monkey(message:types.Message, state:FSMContext):
    if message.text == "Назад":
        await state.reset_state(with_data=False)
        await message.answer(text="Отмена действия", reply_markup=on_start_keyboard())
    else:
        await cargo_damaged(message, state)


# TODO------------------------Авария но не дискотека Авария--------------------------


@dp.message_handler(lambda msg: msg.text == "Авария")
async def accident_very_sowwy(message:types.Message, state:FSMContext):
    msg = '''
    ❗При небольших поломках, в случае которых вы по-прежнему можете продолжить движение, необходимо создать заявку и в
     ней описать проблему. Мы передаем эту заявку и далее с Вами свяжутся. ⛔Если же произошла критическая поломка
      и вы не можете продолжать движение, то необходимо СРОЧНО СВЯЗАТЬСЯ с вашим диспетчером, а также описать поломку(приложить фото)
       в этом чат боте. Детальное описание проблемы с прикрепленными фотографиями позволит принять правильное решение по её устранению.. 
    '''
    await message.answer(text=msg)
    await message.answer(text="Опишите вашу проблему", reply_markup=back())
    await Accident.ACCIDENT_CONTEXT.set()


@dp.message_handler(state=Accident.ACCIDENT_CONTEXT)
async def accident_context_get(message:types.Message, state:FSMContext):
    if message.text == "Назад":
        await state.reset_state(with_data=False)
        await message.answer(text="Отмена действия", reply_markup=on_start_keyboard())
    elif if_user_crazy_monkey_check(["Авария"], message.text):
        await state.reset_state(with_data=False)
        await accident_very_sowwy(message, state)
    else:
        await state.update_data(
            accident_context = message.text
        )
        await message.answer(
            text="Ваша заявка принята. В скором времени к вам подключится оператор для решения вашей проблемы.",
            reply_markup=on_start_keyboard()
        )
        # Пункт 4
        await result(message=message, state=state, situation_type="ACCIDENT")


# TODO-----------------------Полиция---------------------------


@dp.message_handler(lambda msg: msg.text == "Полиция")
async def acab(message:types.Message, state:FSMContext):
    await message.answer(
        text = "Наберите: +380000000000"
    )


# TODO-----------------------Техническая помощь---------------------------

@dp.message_handler(lambda msg: msg.text == "Техническая помощь")
async def tech_supp(message:types.Message, state:FSMContext):
    await message.answer(text="Кратко опишите что случилось и прикрепите фото поломки. "
                              "С вами свяжется служба технической поддержки", reply_markup=technical_support_keyboard())
    USER_KEYBOARDS.append(on_start_keyboard())


@dp.message_handler(lambda msg: msg.text == "Запись на ТО")
async def ask_for_to(message:types.Message, state:FSMContext):
    await message.answer(
        text="Сообщите марку и пробег авто",
        reply_markup=back()
    )
    await TechnicalSupport.ASK_FOR_TO.set()


@dp.message_handler(lambda msg: msg.text == "Проблемы с машиной")
async def car_broken(message:types.Message, state:FSMContext):
    await message.answer(
        text="Кратко опишите что случилось",
        reply_markup=back()
    )
    await TechnicalSupport.CAR_HAS_BEEN_BROKEN.set()


@dp.message_handler(state=TechnicalSupport.CAR_HAS_BEEN_BROKEN)
async def collect_problem_info(message:types.Message, state:FSMContext, flag=False):
    if message.text == "Назад":
        await state.reset_state(with_data=False)
        await message.answer(text="Отмена действия", reply_markup=technical_support_keyboard())
    elif if_user_crazy_monkey_check(["Проблемы с машиной"], message.text):
        await state.reset_state(with_data=False)
        await car_broken(message, state)
    else:
        if not flag:
            await state.update_data(broken_description = message.text)
        await message.answer(text="Прикрепите фото поломки")
        await TechnicalSupport.GET_BROKE_PHOTO.set()


@dp.message_handler(state=TechnicalSupport.GET_BROKE_PHOTO, content_types=types.ContentTypes.ANY)
async def collect_photo(message:types.Message, state:FSMContext):
    if not message.photo:
        await state.reset_state(with_data=False)
        await collect_problem_info(message=message, state=state, flag=True)
    else:
        await state.update_data(
            damage_car_photo=await bot.download_file_by_id(message.photo.pop().file_id)
        )
        await message.answer(
            text="Ваша заявка принята. В скором времени к вам подключится оператор для решения вашей проблемы.",
            reply_markup=technical_support_keyboard()
        )
        await state.reset_state(with_data=False)
        await result(message=message, state=state, situation_type="CAR_BROKEN")


@dp.message_handler(state=TechnicalSupport.ASK_FOR_TO)
async def collect_request(message:types.Message, state:FSMContext):
    if message.text == "Назад":
        await state.reset_state(with_data=False)
        await message.answer(text="Отмена действия", reply_markup=technical_support_keyboard())
    elif if_user_crazy_monkey_check(["Запись на ТО"], message.text):
        await state.reset_state(with_data=False)
        await ask_for_to(message, state)
    else:
        await state.update_data(car_mark_and_type = message.text)
        await message.answer(
            text="Ваша заявка принята. В скором времени к вам подключится оператор для решения вашей проблемы.",
            reply_markup=technical_support_keyboard()
        )
        await result(message=message, state=state, situation_type="TO_REQUEST")

# TODO-----------------------Бухгалтерия---------------------------


@dp.message_handler(lambda msg: msg.text == "Бухгалтерия")
async def buhaltery(message:types.Message, state:FSMContext):
    USER_KEYBOARDS.append(on_start_keyboard())
    await message.answer(text="Выберите интересующюю вас кнопку", reply_markup=buchaltery_keyboard())


@dp.message_handler(lambda msg: msg.text == "Не получил деньги!" or msg.text == "Ошибка в чеке"
                                or msg.text == "Реквизиты компании" or msg.text == "Другое.")
async def first_4_handlers(message:types.Message, state:FSMContext):
    await message.answer(text="Опишите вашу проблему", reply_markup=back())
    await state.update_data(user_button_choice=message.text)
    await BuchalteryStates.GET_INFO4.set()


@dp.message_handler(lambda msg: msg.text == "Как и когда происходит оплата")
async def how_and_when_recieving_money(message: types.Message, state:FSMContext):
    msg = '''Каждую пятницу мы отправляем деньги на бизнес Zelle
     или ACH перевод на ваш бизнес аккаунт. Обычно деньги приходят в течении 2-х рабочих дней.
      Мы ответили на ваш вопрос?'''
    await message.answer(
        text=msg,
        reply_markup=buch_yes_no()
    )
    await BuchalteryStates.YES_NO_QUESTION_STATE.set()


@dp.message_handler(lambda msg: msg.text == "Да" or msg.text == "Нет", state=BuchalteryStates.YES_NO_QUESTION_STATE)
async def callback_yes_no_handler(message:types.Message, state:FSMContext):
    if message.text == "Да":
        await message.answer(text="Выберите интересующюю вас кнопку", reply_markup=buchaltery_keyboard())
        await state.reset_state(with_data=False)
    else:
        await message.answer(
            text="Опишите с чем возникли сложности",
            reply_markup=back()
        )
        await BuchalteryStates.DONT_UNDERSTAND.set()


@dp.message_handler(state=BuchalteryStates.DONT_UNDERSTAND)
async def connect_user(message:types.Message, state:FSMContext):
    if message.text == "Назад":
        await message.answer(
            text="Отмена действия",
            reply_markup=buchaltery_keyboard()
        )
        await state.reset_state(with_data=False)
    elif message.text == "Нет":
        await state.reset_state(with_data=False)
        await callback_yes_no_handler(message, state)
    else:
        await state.update_data(user_difficults = message.text)
        await message.answer(text="Выберите интересующюю вас кнопку", reply_markup=buchaltery_keyboard())
        await result(message, state, situation_type="PROBLEMS_WITH_PAYMENTS")


@dp.message_handler(lambda msg: msg.text == "Депозирование чека")
async def when_and_how_payments_come(message:types.Message, state:FSMContext):
    msg = '''Если в качестве оплаты за доставку вы получили чек, вам необходимо
     задепозировать его на аккаунт компании IDelivery. Что нужно делать:1️⃣ Взять чек 2️⃣ Пойти с чеком в банки 
     Bank of America или WELLS FARGO. 3️⃣ Запросить реквизиты в этом чат боте. Задепозировать чек у менеджера банка в окошке !!
     ВНИМАНИЕ. Мы не берем чеки от частных клиентов, от физических лиц. 
     Берем чеки только от компаний, то есть от юридических лиц.'''
    await message.answer(
        text=msg
    )


@dp.message_handler(lambda msg: msg.text == "Виды оплат за лоад")
async def payments_variations(message:types.Message, state:FSMContext):
    msg = '''Какие бывают формы оплаты?
1.  COP – оплата на загрузке (cash app, zell, venmo, cash, check)
2.  COD – оплата на выгрузке (cash app, zell, venmo, cash, check)
3.  ACH – перевод на компанию
4.  QuickPay– перевод на компанию
5.  5 Days – перевод на компанию (дни могут отличаться)

За оплаты COP/COD Брокер ответственности не несет, т.е. если вы не взяли оплату с клиента, ответственность ложится на вас.

Рекомендуем и настоятельно просим, если у вас стоит данная оплата, вы НЕ ПЕРЕДАЁТЕ груз до тех пор, пока вас не оплатят.

Так же ЗАПРЕЩАЕТСЯ диспетчерам менять форму оплаты, когда водитель находится на доставке. Если такое происходит, большая просьба, написать в чат поддержки.

От частных клиентов чеки не берем!!️
Это одни из самых главных правил!!️
БРОКЕР И КОМПАНИЯ ОТВЕТСТВЕННОСТИ НЕ НЕСУТ!!!
'''
    await message.answer(text=msg)


@dp.message_handler(state=BuchalteryStates.GET_INFO4)
async def collect_msg(message:types.Message, state:FSMContext):
    if message.text == "Назад":
        await state.reset_state(with_data=False)
        await message.answer(text="Отмена действия", reply_markup=buchaltery_keyboard())
    elif if_user_crazy_monkey_check(["Не получил деньги!", "Ошибка в чеке", "Реквизиты компании", "Другое."], message.text):
        await state.reset_state(with_data=False)
        await first_4_handlers(message, state)
    else:
        await message.answer(text="Выберите интересующюю вас кнопку", reply_markup=buchaltery_keyboard())
        await state.update_data(user_problem_description = message.text)
        await state.reset_state(with_data=False)
        await result(message=message, state=state, situation_type="BUCH_4_TYPES")


@dp.message_handler(lambda msg: msg.text == "Отправить фотографию чека")
async def get_user_ticket(message:types.Message, state:FSMContext):
    await BuchalteryStates.GET_TICKET_PHOTO.set()
    await message.answer(text="Вышлите фото чека НЕ БЕРИТЕ ЧЕК НА ЧАСТНОЕ ЛИЦО, только на компанию!", reply_markup=back())


@dp.message_handler(state=BuchalteryStates.GET_TICKET_PHOTO, content_types=types.ContentTypes.ANY)
async def collect_photo(message:types.Message, state:FSMContext):
    if message.text == "Назад":
        await state.reset_state(with_data=False)
        await message.answer(text="Отмена действия", reply_markup=buchaltery_keyboard())
    elif not message.photo:
        await state.reset_state(with_data=False)
        await get_user_ticket(message, state)
    else:
        await state.update_data(
            user_ticket_photo=await bot.download_file_by_id(message.photo.pop().file_id)
        )
        await message.answer(
            text="Ваша заявка принята. В скором времени к вам подключится оператор для решения вашей проблемы.",
            reply_markup=buchaltery_keyboard()
        )
        await state.reset_state(with_data=False)
        await result(message=message, state=state, situation_type="TICKET_PHOTO_PROBLEM")


# TODO----------------------Мои Документы----------------------------


@dp.message_handler(lambda msg: msg.text == "Мои документы")
async def my_documents_handler(message:types.Message, state:FSMContext):
    USER_KEYBOARDS.clear()
    USER_KEYBOARDS.append(on_start_keyboard())
    await message.answer(
        text="Выберите что вас интересует",
        reply_markup=my_documents_keyboard()
    )


@dp.message_handler(lambda msg: msg.text == "Необходимые в рейс документы")
async def give_requires_docs(message:types.Message, state:FSMContext):
    msg = "✅ Driver License\n✅ USDOT & MC Signs\n✅ Lease Agreement\n✅ Medical Examiner Certificate\n✅ Truck Rental Agreement\n"
    msg += "✅ Trailer Rental Agreement\n✅ Свидетельство о страховании (COI)\n✅ Памятка DOT по Logbook"
    await message.answer(
        text=msg
    )


@dp.message_handler(lambda msg: msg.text == "Медицинский сертификат")
async def medical_sertificate(message:types.Message, state:FSMContext):
    msg = "Чтобы оформить Medical Examiner Certificate:\n1️⃣ Открываем гугл/ гугл-карты\n2️⃣ Вводим в поиск CDL/DOT Medical exams\n"
    msg += "3️⃣ Выбираем любую клинику поблизости (смотрим на режим работы!)\n" \
           "4️⃣ Едем туда и оформляем в течение 10 минут " \
           "Организация, которая оформляет MEC в Майами: Light Chiropractic Care, 2500 Hollywood Blvd STE , 201, Hollywood, FL 33020 тел. (754) 816-5976"
    await message.answer(
        text=msg
    )


@dp.message_handler(lambda msg: msg.text == "Страховка COI" or msg.text == "Lease Agreement (контракт)"
                                or msg.text == "Signs")
async def handle_3func_of_docs(message:types.Message, state:FSMContext):
    await message.answer(
        text="Укажите какой документ вы хотите получить?",
        reply_markup=back()
    )
    await state.update_data(user_button_choice=message.text)
    await DocumentsStates.HANDLE_3FUNCTIONS_IN_ONE.set()


@dp.message_handler(state=DocumentsStates.HANDLE_3FUNCTIONS_IN_ONE)
async def collect_data(message:types.Message, state:FSMContext):
    if message.text == "Назад":
        await state.reset_state(with_data=False)
        await message.answer(
            text="Отмена действия",
            reply_markup=my_documents_keyboard()
        )
    elif if_user_crazy_monkey_check(["Страховка COI", "Lease Agreement (контракт)", "Signs"], message.text):
        await state.reset_state(with_data=False)
        await handle_3func_of_docs(message, state)
    else:
        await message.answer(
            text="Ваша заявка принята. В скором времени к вам подключится оператор для решения вашей проблемы.",
            reply_markup=my_documents_keyboard()
        )
        await state.update_data(user_requested_doc = message.text)
        await state.reset_state(with_data=False)
        await result(message, state, situation_type="REQUESTED_DOC")


# TODO------------------------Топливная Карта--------------------------


@dp.message_handler(lambda msg: msg.text == "Топливная карта")
async def fuel_card_start_menu(message:types.Message, state:FSMContext):
    await message.answer(
        text="Выберите что вас интересует",
        reply_markup=fuel_card_start()
    )
    USER_KEYBOARDS.clear()
    USER_KEYBOARDS.append(on_start_keyboard())


@dp.message_handler(lambda msg: msg.text == "Работа с топливной картой" or msg.text == "Вас интересует как пользоваться топливной картой")
async def working_with_fuel_card(message:types.Message, state:FSMContext):
    await message.answer(
        text="Выберите интересующий вас вопрос из списка",
        reply_markup=how_to_work_with_fuel_card()
    )
    USER_KEYBOARDS.append(fuel_card_start())


@dp.message_handler(lambda msg: msg.text == "Схемы работы по топливным картам")
async def scheme_with_cards(message:types.Message, state:FSMContext):
    msg = '''
СХЕМЫ РАБОТЫ ПО ТОПЛИВНЫМ КАРТАМ   Для того, чтобы упростить контроль расходов, избежать лишних расходов на топливо и упростить бухгалтерию   мы предлагаем вам выбрать один из двух вариантов, описанных ниже:   
🔸 вариант #1 - вы заправляетесь ВСЕГДА ТОЛЬКО по топливным картам и высылаете на счёт компании весь кэш, полученный за доставки от клиентов (CashApp, Venmo, Zell, Check и т.п.) и не используете его для оплаты топлива   
🔹 вариант #2 - для оплаты ВСЕГДА вы используете кэш, полученный на доставках, тогда топливные карты НЕ ДОЛЖНЫ вами использоваться   То есть предлагаем вам выбрать 1 из 2 вариантов: всегда используются либо ТОПЛИВНЫЕ КАРТЫ, либо КЭШ с доставок
'''
    await message.answer(text=msg)


@dp.message_handler(lambda msg: msg.text == "Виртуальные топливные карты")
async def virtual_fuel_cards(message:types.Message, state:FSMContext):
    msg = '''⛽ВИРТУАЛЬНЫЕ ТОПЛИВНЫЕ КАРТЫ:Инструкции по работе с виртуальной топливной картой:   
1️⃣ Скачать приложение Pilot Flying 
2️⃣ Посмотреть видео-инструкцию: https://www.youtube.com/watch?v=W_GgVwmOe2g 
3️⃣ Выдается номер карты
4️⃣ Прикрепить в приложении 
5️⃣ Это НЕ rewards card. Поэтому в приложении есть раздел Wallet. Туда и нужно ее закрепить. 
6️⃣ Выдается DriverID = он же PIN
7️⃣ Заправляться на тех же заправках, что и фуры!  
⭕️ В случае, когда карта прикреплена в приложении, но Mobile App is not avaliable: Нужно зайти внутрь, обратиться на кассу, обьяснить ситуацию и продиктовать номер кассиру. 12/40 - это дата окончания срока карты   https://www.youtube.com/watch?v=W_GgVwmOe2g'''
    await message.answer(
        text=msg,
        reply_markup=virtual_fuel_cards_keyboard()
    )
    USER_KEYBOARDS.append(how_to_work_with_fuel_card())


@dp.message_handler(lambda msg: msg.text == "Получить номер топливной карты")
async def get_fuel_card_number(message:types.Message, state:FSMContext):
    await state.update_data(user_id=message.from_user.id)
    await result(message, state, situation_type="GET_FUEL_CARD_NUMBER")
    await message.answer(
        text="Ваша заявка принята. В скором времени к вам подключится оператор для решения вашей проблемы."
    )


@dp.message_handler(lambda msg: msg.text == "Пластиковые топливные карты")
async def plastic_fuel_cards(message:types.Message, state:FSMContext):
    msg = '''ПЛАСТИКОВЫЕ ТОПЛИВНЫЕ КАРТЫ:
Пластиковую топливную карту Pilot вы можете получить двумя способами:'''
    await message.answer(
        text=msg,
        reply_markup=plastic_fuel_cards_keyboard()
    )
    USER_KEYBOARDS.append(how_to_work_with_fuel_card())


@dp.message_handler(lambda msg: msg.text == "Заказать на почту на выбранный адрес компании"
                                or msg.text == "Забрать в офисе компании")
async def request_for_receiving_fuel_card(message:types.Message, state:FSMContext):
    await message.answer(
        text="Ваша заявка принята. В скором времени к вам подключится оператор для решения вашей проблемы."
    )
    await state.update_data(user_button_choice=message.text)
    await state.update_data(user_id=message.from_user.id)
    await result(message, state, situation_type="ASKING_FOR_RECIEVING_FUEL_CARD")


@dp.message_handler(lambda msg: msg.text == "Не проходит транзакция" or msg.text == "Отклоняет оплату")
async def transaction_fuel_card_error(message:types.Message, state:FSMContext):
    msg = '''Заправляться по номеру карты на кассе: В случае, когда карта прикреплена в приложении, но Mobile App is not avaliable:
Нужно зайти внутрь, обратиться на кассу, обьяснить ситуацию и продиктовать номер кассиру. 12/40 - это дата окончания срока карты Driver ID'''

    await message.answer(
        text="Попробуйте заправиться по топливной карте! Ниже я приложу инструкцию!"
    )
    await message.answer(
        text=msg, reply_markup=buch_yes_no()
    )
    await FuelCardsStates.YES_NO_QUESTION.set()


@dp.message_handler(state=FuelCardsStates.YES_NO_QUESTION)
async def collect_answer(message:types.Message, state:FSMContext):
    if message.text == "Да":
        await message.answer(
            text="Отлично",
            reply_markup=fuel_card_start()
        )
    elif message.text == "Нет":
        await message.answer(
            text="Опишите что у вас произошло", reply_markup=back()
        )
        await FuelCardsStates.NO_PROBLEM_TRANSACTION.set()
    else:
        await message.answer(text="Пожалуйста выберите одну из кнопок")
        await state.reset_state(with_data=False)
        await transaction_fuel_card_error(message, state)


@dp.message_handler(state=FuelCardsStates.NO_PROBLEM_TRANSACTION)
async def transaction_problem_connecting_to_dispatch(message:types.Message, state:FSMContext):
    if message.text == "Назад":
        await state.reset_state(with_data=False)
        await message.answer(
            text="Отмена действия",
            reply_markup=fuel_card_start()
        )
    else:
        await state.update_data(description_transaction_problem=message.text)
        await state.reset_state(with_data=False)
        await message.answer(
            text="Ваша заявка принята. В скором времени к вам подключится оператор для решения вашей проблемы.",
            reply_markup=fuel_card_start()
        )
        await result(message, state, situation_type="TRANSACTION_FUEL_CARD_PROBLEM")


@dp.message_handler(lambda msg: msg.text == "Другoе")
async def other_fuel_cards(message:types.Message, state:FSMContext):
    await message.answer(
        text="Опишите что у вас произошло", reply_markup=back()
    )
    await FuelCardsStates.OTHER_FUEL.set()


@dp.message_handler(state=FuelCardsStates.OTHER_FUEL)
async def collect_info_from_other(message:types.Message, state:FSMContext):
    if message.text == "Назад":
        await state.reset_state(with_data=False)
        await message.answer(
            text="Отмена действия",
            reply_markup=fuel_card_start()
        )
    else:
        await state.update_data(other_fuel_problem = message.text)
        await state.update_data(user_id = message.from_user.id)
        await state.reset_state(with_data=False)
        await result(message, state, situation_type="OTHER_FUEL_CARD_PROBLEM")


# TODO--------------------------------------------------


@dp.message_handler(lambda msg: msg.text == "Страховкa")
async def insurance_on_start(message:types.Message, state:FSMContext):
    await message.answer(
        text="Выберите что вас интересует",
        reply_markup=insurance_start_keyboard()
    )
    USER_KEYBOARDS.clear()
    USER_KEYBOARDS.append(on_start_keyboard())


@dp.message_handler(lambda msg: msg.text in ["Cтрахoвкa", "Сумма страховки не соответствует ранее заявленной", "Страховой случай", "Другоe"])
async def collect_data_from_insurance(message:types.Message, state:FSMContext):
    await message.answer(
        text="Опишите вашу ситуацию", reply_markup=back()
    )
    await state.update_data(user_button_choice = message.text)
    await Insurance.GET_DATA.set()


@dp.message_handler(state=Insurance.GET_DATA)
async def collect_insurance_data(message:types.Message, state:FSMContext):
    if message.text == "Назад":
        await state.reset_state(with_data=False)
        await message.answer(
            text="Отмена действия",
            reply_markup=insurance_start_keyboard()
        )
    else:
        await state.update_data(insurance_info = message.text)
        await message.answer(
            text="Ваша заявка принята. В скором времени к вам подключится оператор для решения вашей проблемы.",
            reply_markup=insurance_start_keyboard()
        )
        await result(message, state, situation_type="INSURANCE_PROBLEM")


# TODO---------------------ТРАК/ТРЕЙЛЕР-----------------------------

@dp.message_handler(lambda msg: msg.text == "Приемка трака/трейлера")
async def give_user_tracks_keys(message:types.Message, state:FSMContext):
    await message.answer(
        text="Выберите что вас интересует",
        reply_markup=tracks()
    )
    USER_KEYBOARDS.clear()
    USER_KEYBOARDS.append(on_start_keyboard())


@dp.message_handler(lambda msg: msg.text == "Трак" or msg.text == "Трейлер")
async def tracks_setup(message:types.Message, state:FSMContext):
    if message.text == "Трак":
        await message.answer(
            text='''Приемка/передача трака
✅ При сдаче трака надо провести вот такую фото-инспекцию и отправить в чат. При получении трака (если Вы новый водитель/оунер) - надо сделать то же самое.'''
        )
    elif message.text == "Трейлер":
        await message.answer(
            text='''Приемка/передача трейлера
✅ Предметы - это опционально, в зависимости от того, Вы это приобретали или
нет. При сдаче трейлера надо провести вот такую фото-инспекцию и отправить
в чат. При получении трейлера (если вы новый водитель/оунер) - надо сделать
то же самое.'''
        )

# TODO--------------------------Аренда------------------------


@dp.message_handler(lambda msg: msg.text == "Отдел аренды")
async def rent_handler(message:types.Message, state:FSMContext):
    await message.answer(
        text="Выберите что вас интересует",
        reply_markup=rent_keyboard()
    )
    USER_KEYBOARDS.clear()
    USER_KEYBOARDS.append(on_start_keyboard())


@dp.message_handler(lambda msg: msg.text == "Машина" or msg.text == "Прицеп")
async def rent_situation(message:types.Message, state:FSMContext):
    await message.answer(
        text="Опишите ваше обращение",
        reply_markup=back()
    )
    await state.update_data(user_button_choice=message.text)
    await RentState.COLLECT_INFO.set()


@dp.message_handler(state=RentState.COLLECT_INFO)
async def collect_rent_info(message:types.Message, state:FSMContext):
    if message.text == "Назад":
        await state.reset_state(with_data=False)
        await message.answer(
            text="Отмена действия",
            reply_markup=rent_keyboard()
        )
    else:
        await state.update_data(tracks_request=message.text)
        await message.answer(
            text="Ваша заявка принята. В скором времени к вам подключится оператор для решения вашей проблемы.",
            reply_markup=rent_keyboard()
        )
        await result(message, state, situation_type="RENT_REQUEST")


# TODO--------------------------------------------------


@dp.message_handler(lambda msg:msg.text == "Дpyгoe")
async def main_other_menu(message:types.Message, state:FSMContext):
    await message.answer(
        text="Напишите что вам требуется?",
        reply_markup=back()
    )
    await MainOtherState.OTHER_PUBLIC_STATE.set()


@dp.message_handler(state=MainOtherState.OTHER_PUBLIC_STATE)
async def collect_other_public_info(message:types.Message, state:FSMContext):
    if message.text == "Назад":
        await state.reset_state(with_data=False)
        await message.answer(
            text="Отмена действия",
            reply_markup=on_start_keyboard()
        )
    else:
        await message.answer(
            text="Ваша заявка принята. В скором времени к вам подключится оператор для решения вашей проблемы.",
            reply_markup=on_start_keyboard()
        )
        await state.update_data(other_info=message.text)
        await result(message, state, situation_type="OTHER_USER_ASK")


# TODO--------------------------------------------------

@dp.message_handler(lambda msg: msg.text == "Назад")
async def cum_on_back(message:types.Message, state:FSMContext):
    try:
        await message.answer("Вы вернулись назад", reply_markup=USER_KEYBOARDS.pop())
    except IndexError:
        await message.answer(text="Переход в стартовое меню", reply_markup=on_start_keyboard())


@dp.message_handler(lambda msg: True)
async def catch_all_messages(message:types.Message, state:FSMContext):
    user_message = message.text.lower()
    if re.findall(form_fuel_re(), user_message):
        await fuel_card_start_menu(message, state)
    elif re.findall(form_my_docs_re(), user_message):
        await my_documents_handler(message, state)
    elif re.findall(form_police_re(), user_message):
        await acab(message, state)
    elif re.findall(form_tracks_re(), user_message):
        await tracks_setup(message, state)
    elif re.findall(form_rent_re(), user_message):
        await rent_handler(message, state)
    elif re.findall(form_tech_supp_re(), user_message):
        await tech_supp(message, state)
    elif re.findall(form_buch_re(), user_message):
        await buhaltery(message, state)
    else:
        await message.answer(
            text="Пожалуйста выберите интересующюю вас кнопку", reply_markup=on_start_keyboard()
        )
        USER_KEYBOARDS.clear()


async def result(message:types.Message, state:FSMContext, situation_type):
    data = await state.get_data()
    # data["Ситуация"] = situation_type
    # await bot.send_message(text=f"{data}", chat_id=message.from_user.id)
    await state.reset_state(with_data=True)
    if situation_type == "CARGO_DAMAGED":
        context_situation = data.get("damaged_situation_description")
        photo = data.get("damage_car_photo")
        # await bot.send_message(text=f"Ситуация: {situation_type}\n", chat_id=message.from_user.id)
        await bot.send_photo(chat_id=message.from_user.id,photo=photo.read(), caption=f"Ситуация: {situation_type}\n"
                                                                                      f"Описание: {context_situation}\n"
                                                                                      f"Айди пользователя: {message.from_user.id}")

    elif situation_type == "ACCIDENT":
        context_situation = data.get("accident_context")
        await bot.send_message(chat_id=message.from_user.id, text=f"Ситуация: {situation_type}\n"
                                                                  f"Описание: {context_situation}\n"
                                                                  f"Айди пользователя: {message.from_user.id}")

    elif situation_type == "TO_REQUEST":
        car_mark_and_type = data.get("car_mark_and_type")
        await bot.send_message(chat_id=message.from_user.id, text=f"Ситуация: {situation_type}\n"
                                                                  f"Марка и пробег: {car_mark_and_type}\n"
                                                                  f"Айди пользователя: {message.from_user.id}")

    elif situation_type == "CAR_BROKEN":
        photo = data.get("damage_car_photo")
        context_situation = data.get("broken_description")
        await bot.send_photo(chat_id=message.from_user.id, photo=photo.read(), caption=f"Ситуация: {situation_type}\n"
                                                                                       f"Описание: {context_situation}\n"
                                                                                       f"Айди пользователя: {message.from_user.id}")

    elif situation_type == "BUCH_4_TYPES":
        usr_choice = data.get("user_button_choice")
        descr = data.get("user_problem_description")
        await bot.send_message(chat_id=message.from_user.id, text=f"Ситуация: {situation_type}\n"
                                                                  f"Выбор пользователя: {usr_choice}\n"
                                                                  f"Описание: {descr}\nАйди пользователя: {message.from_user.id}")
    elif situation_type == "TICKET_PHOTO_PROBLEM":
        photo = data.get("user_ticket_photo")
        await bot.send_photo(chat_id=message.from_user.id, photo=photo.read(), caption=f"Ситуация: {situation_type}\n"
                                                                                       f"Айди пользователя: {message.from_user.id}")

    elif situation_type == "REQUESTED_DOC":
        usr_choice = data.get("user_button_choice")
        descr = data.get("user_requested_doc")
        await bot.send_message(chat_id=message.from_user.id, text=f"Ситуация: {situation_type}\n"
                                                                  f"Выбор пользователя: {usr_choice}\n"
                                                                  f"Описание: {descr}\nАйди пользователя: {message.from_user.id}")

    elif situation_type == "GET_FUEL_CARD_NUMBER":
        await bot.send_message(chat_id=message.from_user.id, text=f"Ситуация: {situation_type}\n"
                                                                  f"Айди пользователя: {data.get('user_id')}")

    elif situation_type == "ASKING_FOR_RECIEVING_FUEL_CARD":
        await bot.send_message(chat_id=message.from_user.id, text=f"Ситуация: {situation_type}\n"
                                                                  f"Айди пользователя: {data.get('user_id')}\n"
                                                                  f"Выбор пользователя: {data.get('user_button_choice')}")
    elif situation_type == "TRANSACTION_FUEL_CARD_PROBLEM":
        await bot.send_message(chat_id=message.from_user.id, text=f"Ситуация: {situation_type}\nОписание: {data.get('description_transaction_problem')}\nАйди пользователя: {message.from_user.id}")

    elif situation_type == "OTHER_FUEL_CARD_PROBLEM":
        await bot.send_message(chat_id=message.from_user.id, text=f"Ситуация: {situation_type}\n"
                                                                  f"Описание: {data.get('description_transaction_problem')}\n"
                                                                  f"Айди пользователя: {data.get('user_id')}")
    # elif situation_type == "TRACKS_REQUEST":
    #     await bot.send_message(chat_id=message.from_user.id, text="")
    elif situation_type == "RENT_REQUEST":
        await bot.send_message(chat_id=message.from_user.id, text=f"Ситуация: {situation_type}\n"
                                                                  f"Выбор пользователя: {data.get('user_button_choice')}\n"
                                                                  f"Описание: {data.get('tracks_request')}\nАйди пользователя: {message.from_user.id}")
    elif situation_type == "OTHER_USER_ASK":
        await bot.send_message(chat_id=message.from_user.id, text=f"Ситуация: {situation_type}\nОписание: {data.get('other_info')}\nАйди пользователя: {message.from_user.id}")
    elif situation_type == "PROBLEMS_WITH_PAYMENTS":
        await bot.send_message(chat_id=message.from_user.id, text=f"Ситуация: {situation_type}\nОписание: {data.get('user_difficults')}\nАйди пользователя: {message.from_user.id}")
    elif situation_type == "INSURANCE_PROBLEM":
        await bot.send_message(chat_id=message.from_user.id, text=f"Ситуация: {situation_type}\n"
                                                                  f"Выбор пользователя: {data.get('user_button_choice')}\n"
                                                                  f"Описание: {data.get('insurance_info')}"
                                                                  f"\nАйди пользователя: {message.from_user.id}")
    # phone = data.get("phone_number")
    # await state.reset_data()
    await state.reset_state(with_data=True)
    # await state.update_data(phone_number=phone)


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp)
