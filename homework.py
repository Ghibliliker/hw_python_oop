# калькулятор денег и калорий
# пользователь создает калькулятор и может вести учет
# базовой валютой были взяты белорусские рубли - автор патриот :)
import datetime as dt


class Calculator:
    def __init__(self, limit: int):
        self.limit = limit
        self.records = []

    def add_record(self, obj: 'Record') -> None:
        """Добавляем запись в память."""
        self.records.append(obj)

    def get_today_stats(self) -> float:
        """Рассчет потраченных единиц за сутки."""
        count = 0
        now = dt.date.today()
        for record in self.records:
            if record.date == now:
                count += record.amount
        return count

    def get_week_stats(self) -> float:
        """Рассчет потраченных единиц за неделю."""
        count = 0
        one_week = dt.timedelta(days=7)
        now = dt.date.today()
        for record in self.records:
            if record.date <= now and record.date >= now - one_week:
                count += record.amount
        return count


class CaloriesCalculator(Calculator):

    def get_calories_remained(self) -> str:
        """Рассчет остатка и сравнение с лимитом"""
        how_today = self.get_today_stats()
        how_end = self.limit - how_today
        if how_end > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей'
                    f' калорийностью не более {round(how_end, 2)} кКал')
        else:
            return 'Хватит есть!'

    def get_today(self) -> str:
        """Рассчет набранных калорий за день и вывод."""
        answer = self.get_today_stats()
        return f'За сегодня вы накушали {round(answer, 2)} калорий!'

    def get_week(self) -> str:
        """Рассчет набранных калорий за неделю и вывод."""
        answer = self.get_week_stats()
        return f'За прошедшую неделю вы накушали {round(answer, 2)} калорий!'


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0

    def __init__(self, limit: int):
        super().__init__(limit)

    def exchanger(self, money: float, currency: str) -> (float, str):
        """Перевод в запрашиваемую валюту"""
        if currency == 'rub':
            return round(money, 2), 'руб'
        elif currency == 'usd':
            answer = money / CashCalculator.USD_RATE
            return round(answer, 2), 'USD'
        elif currency == 'eur':
            answer = money / CashCalculator.EURO_RATE
            return round(answer, 2), 'Euro'
        else:
            print('Неизвестная валюта, потому выводим в рублях.')
            return round(money, 2), 'руб'

    def get_today_cash_remained(self, currency: str) -> str:
        """Рассчет остатка и сравнение с лимитом."""
        how_today = self.get_today_stats()
        how_end = self.limit - how_today
        if how_end > 0:
            answer, name = self.exchanger(how_end, currency)
            return f'На сегодня осталось {answer} {name}'
        elif how_end == 0 and currency in ('rub', 'eur', 'usd'):
            return 'Денег нет, держись'
        elif how_end < 0:
            answer, name = self.exchanger(how_end, currency)
            return f'Денег нет, держись: твой долг - {abs(answer)} {name}'
        else:
            return 'Все пошло не по плану!'

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


class Record:
    def __init__(self, amount: int, comment: str, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
