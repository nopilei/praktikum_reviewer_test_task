# Можно написать "from datetime import datetime as dt", то есть импортировать
# не сам модуль datetime, а класс внутри него, чтобы сократить код, где идет
# работа с датой.
import datetime as dt


class Record:
    # Здесь лучше не date='', а date=None.
    #
    # None хорош тем, что он имеет четкое назначение - задать логически
    # "отсутствие" чего-нибудь.  Если мы видим в сигнатуре функции (часть
    # функции, содержащая имя и параметры) что один из параметров будет
    # по умолчанию равен None, то мы можем с уверенностью предположить,
    # что далее в теле функции этот параметр будет проверяться на истинность
    # (или на соответствие самому None) в условии с if.
    # Например:
    #
    # if date:
    #     <какой-то код>
    #
    # ИЛИ
    #
    # if not date:
    #     <какой-то код>
    #
    # ИЛИ
    #
    # if date is None:
    #     <какой-то код>
    #
    # ИЛИ
    #
    # if date is not None:
    #     <какой-то код>
    #
    # Соответственно, это улучшает читабельность/усваиваемость кода.  Если мы
    # пишем date='', то другие, кто будет читать ваш код, будут ожидать,
    # например, что дальше date будет сравниваться с другой строкой.
    # Задумайтесь, почему вы написали именно date='', а не date=0, например?
    # Возможно, вы тем самым хотели указать на то, что date должен быть
    # строкой.  Но для этой цели в Python есть type annotations.
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Лучше читается так:
        #
        # self.date = (
        #     dt.datetime.now().date() if not date
        #     else dt.datetime.strptime(date, '%d.%m.%Y').date()
        # )
        #
        # Или можно по-простому:
        #
        # if not date:
        #     self.date = dt.datetime.now().date()
        # else:
        #     self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        # В Python очень часто удается элегантно заменять рутинные для других
        # языков программирования операции, такие как эта (объявить
        # переменную, пробежаться по массиву данных в цикле, проверяя на
        # каждой итерации соответствие условию, и если все ок,
        # добавить к переменной элемент массива). С использованием функции
        # sum, тело этого метода может выглядеть так
        #
        # return sum(
        #    record.amount for record in self.records
        #    if record.date == dt.datetime.now().date()
        # )
        today_stats = 0
        # В большинстве случаев, переменная в цикле for должна начинаться с
        # маленькой буквы. Более того, имя Record уже используется (объявление
        # класса Record).  Правильнее будет for record in self.records:
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                # Более читабельно today_stats += record.amount
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        # Также можно переписать с sum (см. выше)
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # В Python можно написать if 0 <= (today - record.date).days < 7:
            # что лучше читается
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Комментарий ниже лучше оформить в виде docstring, потому что это
    # описание того, что делает функция.
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Согласно PEP 8, для продолжения строки кода лучше оборачивать
            # ее в круглые скобки вместо обратного слэша в конце.
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # Ненужный else
        else:
            # Ненужные скобки.  Выражение ассоциируется с кортежем, а не
            # строкой.
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Имена параметров в сигнатуре должны писаться в нижнем регистре.  Кроме
    # того, USD_RATE и EURO_RATE по условию задания в объявлении этого метода
    # быть не должны.  Если вы хотите, чтобы курс валют выбирался, лучше
    # это сделать в .__init__(), например:
    #
    #   def __init__(self, usd_rate=USD_RATE, euro_rate=EURO_RATE):
    #       self.usd_rate = usd_rate
    #       self.euro_rate = euro_rate
    #
    # и затем использовать self.usd_rate и self.euro_rate.
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # При объявлении переменной не стоит присваивать ей произвольное
        # значение.  currency_type не равен currency по смыслу, поэтому лучше
        # просто currency_type = ''.  К тому же, currency_type не самое удачное
        # название, лучше, например, currency_verbose, оно более явно указывает
        # на назначение переменной (создание читаемой строки)
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # В ситуации, когда у нас множество однотипных блоков elif можно
        # использовать прием со словарем вместо блока if-elif-else:
        #
        #         currency_to_rate_and_type = {
        #             'usd': (self.USD_RATE, 'USD'),
        #             'eur': (self.EURO_RATE, 'USD'),
        #             'rub': (1, 'руб'),
        #         }
        #         try:
        #             rate, currency_type = currency_to_rate_and_type[currency]
        #         except KeyError:
        #             return 'Неправильный выбор'
        #         cash_remained = (self.limit - self.get_today_stats()) / rate
        #
        # Такой подход дает ряд преимуществ: Легче добавить новую валюту,
        # меньше риск сделать ошибку, легче читать код.  Также можно
        # присмотреться к pattern matching в Python 3.10
        #
        #
        #
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Ошибка. Правильно cash_remained /= 1.00, или просто убрать эту
            # строку
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            # По условию задания, в f-строках не должно быть вызовов функций.
            # Также надо иметь в виду особенности работы функции round в
            # Python.  Если нам важна точность при работе с дробными числами,
            # (а если это калькулятор денег, то скорее всего важна), то стоит
            # использовать возможности стандартного модуля decimal
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # Вместо .format() лучше использовать f-строку, как и было выше.
            #
            # Согласно PEP 8, для продолжения строки кода лучше оборачивать
            # ее в круглые скобки вместо обратного слэша в конце.
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    def get_week_stats(self):
        # Метод .get_week_stats() уже имеется в родительском классе Calculator,
        # и переопределять его не нужно.  К тому же не хватает return в начале
        # строки
        super().get_week_stats()
