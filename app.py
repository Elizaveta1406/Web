from flask import Flask, request, render_template, redirect, url_for, flash
import requests
import re

app = Flask(__name__)
app.secret_key = 'sdfghuj8765ef74drtvb8765tcfvyguy766'

API_KEY = 'ecf8be78cbf44e0bb963b676bb18c04f'
API_URL = 'https://openexchangerates.org/api/latest.json'

CURRENCIES = {
    "RUB": "Российский рубль",
    "USD": "Доллар США",
    "EUR": "Евро",
    "CNY": "Китайский юань",
    "KZT": "Казахстанский тенге",
    "PLN": "Польский злотый",
    "TRY": "Турецкая лира",
    "AED": "Дирхам ОАЭ",
    "CHF": "Швейцарский франк"
}


def get_exchange_rates():
    response = requests.get(f"{API_URL}?app_id={API_KEY}")
    return response.json()["rates"]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        amount = request.form.get('amount')
        from_currency = request.form.get('from_currency')
        to_currency = request.form.get('to_currency')

        if not re.match(r'^\d+(\.\d+)?$', amount):
            flash("Некорректный ввод. Введите положительное число.")
            return redirect(url_for('index'))

        amount = float(amount)

        if amount < 0:
            flash("Некорректный ввод. Введите положительное число.")
            return redirect(url_for('index'))

        rates = get_exchange_rates()
        converted_amount = amount * rates[to_currency] / rates[from_currency]

        return render_template('index.html',
                               currencies=CURRENCIES,
                               converted_amount=converted_amount,
                               from_currency=from_currency,
                               to_currency=to_currency,
                               amount=amount)

    return render_template('index.html', currencies=CURRENCIES)


if __name__ == '__main__':
    app.run(debug=True)