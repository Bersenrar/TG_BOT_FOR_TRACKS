import re


def form_fuel_re():
    return r"(картой|топливо|топливная|топливной)"


def form_police_re():
    return r"(полиция|штраф)"


def form_my_docs_re():
    return r"(документы|договор|сайты|распечатки|разрешения)"


def form_buch_re():
    return r"(чек|чеки|чеку|деньги|перевод|перевести деньги|Оплата счета|счет)"


def form_tech_supp_re():
    return r"(тех помощь|ремонт|тех обслуживание|то|поломка)"


def form_rent_re():
    return r"(смена авто|смена трака|замена авто|замена трака|замена прицепа|поменять машину|как правильно сделать осмотр трейлера|как правильно сделать осмотр трака)"


def form_tracks_re():
    return r"(осмотр|инспекция)"

