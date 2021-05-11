"""
Калькулятор денег и калорий
пользователь создает калькулятор и может вести учет
базовой валютой были взяты белорусские рубли - автор патриот :)
"""
import datetime as dt
from typing import Optional, Union


class Record:
    DATE_STR = '%d.%m.%Y'

    def __init__(self, amount: int, comment: str, date: Optional[str] = None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, Record.DATE_STR).date()


class Calculator:
    def __init__(self, limit: int):
        self.limit = limit
        self.records = []

    def add_record(self, obj: 'Record') -> None:
        """Добавляем запись в память."""
        self.records.append(obj)

    def get_balance(self) -> float:
        return self.limit - self.get_today_stats()

    def get_today_stats(self) -> float:
        """Рассчет потраченных единиц за сутки."""
        now = dt.date.today()
        return sum(x.amount for x in self.records if x.date == now)

    def get_week_stats(self) -> float:
        """Рассчет потраченных единиц за неделю."""
        one_w = dt.timedelta(days=7)
        now = dt.date.today()
        now_no_w = now - one_w
        return sum(x.amount for x in self.records if now >= x.date > now_no_w)


class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> str:
        """Рассчет остатка и сравнение с лимитом"""
        x = self.get_balance()
        x_fin = round(x, 2)
        if x_fin > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей'
                    f' калорийностью не более {x_fin} кКал')
        return 'Хватит есть!'

    def get_today(self) -> str:
        """Рассчет набранных калорий за день и вывод."""
        answer = self.get_today_stats()
        x = round(answer, 2)
        return f'За сегодня вы накушали {x} калорий!'

    def get_week(self) -> str:
        """Рассчет набранных калорий за неделю и вывод."""
        answer = self.get_week_stats()
        x = round(answer, 2)
        return f'За прошедшую неделю вы накушали {x} калорий!'


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1.0
    currency_info = {'rub': (RUB_RATE, 'руб'),
                     'usd': (USD_RATE, 'USD'),
                     'eur': (EURO_RATE, 'Euro')}

    def exchanger(self, money: float, currency: str) -> Union[float, str]:
        """Перевод в запрашиваемую валюту"""
        rate, title = self.currency_info[currency]
        if rate and title:
            answer = money / rate
            return round(answer, 2), title
        raise ValueError

    def get_today_cash_remained(self, currency: str) -> str:
        """Рассчет остатка и сравнение с лимитом."""
        x = self.get_balance()
        if x > 0:
            answer, name = self.exchanger(x, currency)
            return f'На сегодня осталось {answer} {name}'
        elif x == 0 and currency in ('rub', 'eur', 'usd'):
            return 'Денег нет, держись'
        else:
            answer, name = self.exchanger(x, currency)
            answer_fin = abs(answer)
            return f'Денег нет, держись: твой долг - {answer_fin} {name}'

    def get_today(self, currency: str) -> str:
        """Рассчет потраченных денег за день и вывод."""
        money = self.get_today_stats()
        answer = self.exchanger(money, currency)
        return f'За сегодня вы потратили {answer} {currency} !'

    def get_week(self, currency: str) -> str:
        """Расчет потраченных денег за неделю и вывод."""
        money = self.get_week_stats()
        answer = self.exchanger(money, currency)
        return f'За прошедшую неделю вы потратили {answer} {currency} !'
