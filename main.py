from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.core.window import Window

# Задаём размер окна для тестирования
Window.size = (350, 600)

class ConverterLayout(BoxLayout):
    result = StringProperty('0.00')

    # Курсы валют — теперь внутри класса как атрибут
    rates = {
        'RUB_USD': 0.011,
        'RUB_EUR': 0.010,
        'USD_RUB': 90.0,
        'USD_EUR': 0.93,
        'EUR_RUB': 98.0,
        'EUR_USD': 1.07
    }

    def convert(self):
        try:
            # Получаем текст из поля ввода
            amount_text = self.ids.input_amount.text
            if not amount_text:
                amount_text = "0"

            amount = float(amount_text)
            from_currency = self.ids.from_spinner.text
            to_currency = self.ids.to_spinner.text

            # Если валюты одинаковые — просто возвращаем сумму
            if from_currency == to_currency:
                self.result = f"{amount:.2f}"
                return

            rate_key = f"{from_currency}_{to_currency}"

            # Проверяем, есть ли такой курс
            if rate_key not in self.rates:
                # Пробуем обратный курс, если прямого нет
                reverse_key = f"{to_currency}_{from_currency}"
                if reverse_key in self.rates:
                    # Пересчитываем через обратный курс
                    self.result = f"{round(amount / self.rates[reverse_key], 2):.2f}"
                else:
                    self.result = "Недоступная конвертация"
                return

            self.result = f"{round(amount * self.rates[rate_key], 2):.2f}"

        except ValueError:
            self.result = "Ошибка: введите число"
        except Exception:
            self.result = "Произошла ошибка"


class CurrencyConverterApp(App):
    def build(self):
        return ConverterLayout()

if __name__ == '__main__':
    CurrencyConverterApp().run()
