import tkinter as tk
from tkinter import ttk
import requests

# Neste campo está a minha chave da API https://www.exchangerate-api.com/
api_key = '4b8338fc26d0402ef92f598a'

# Lista de moedas disponíveis na API
currency_list = ["USD", "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHF", "CLP", "CNY", "COP", "CRC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "FOK", "GBP", "GEL", "GGP", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HRK", "HTG", "HUF", "IDR", "ILS", "IMP", "INR", "IQD", "IRR", "ISK", "JEP", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KID", "KMF", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SLL", "SOS", "SRD", "SSP", "STN", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TVD", "TWD", "TZS", "UAH", "UGX", "UYU", "UZS", "VES", "VND", "VUV", "WST", "XAF", "XCD", "XDR", "XOF", "XPF", "YER", "ZAR", "ZMW", "ZWL"]

def get_exchange_rates():
    url = f'https://v6.exchangerate-api.com/v6/4b8338fc26d0402ef92f598a/latest/USD'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve erro com a chave da API
        data = response.json()
        return data
    except requests.exceptions.RequestException:
        raise Exception('Chave da API não encontrada.')

# Retira o case sensitive
def convert_currency():
    from_currency = from_currency_variable.get().upper()
    to_currency = to_currency_variable.get().upper()
    amount = amount_entry.get()

    # Verifica se as moedas inseridas são válidas
    if from_currency not in currency_list or to_currency not in currency_list:
        result_label.config(text='Moedas inválidas. Selecione moedas válidas.')
        return

    try:
        amount = float(amount)
    except ValueError:
        result_label.config(text='Valor inválido. Insira um valor numérico.')
        return

    try:
        data = get_exchange_rates()
        if from_currency in data['conversion_rates'] and to_currency in data['conversion_rates']:
            conversion_rate = data['conversion_rates'][to_currency] / data['conversion_rates'][from_currency]
            converted_amount = amount * conversion_rate
            result_label.config(text=f'{amount} {from_currency} é igual a {converted_amount:.2f} {to_currency}')
        else:
            result_label.config(text='As moedas não estão na lista de taxas de câmbio.')
    except Exception as e:
        result_label.config(text=f'Erro: {str(e)}')

# Tkinter para criar a interface
root = tk.Tk()
root.title('Conversor de Moedas')

# Tamanho da janela
root.geometry("480x260")

# Cor de fundo
root.config(bg="#202630")

# Label para indicar as caixas de seleção de moeda, valor convertido e resultado
from_currency_label = tk.Label(root, text='Moeda de Origem:', bg="#202630", fg="white", font=('Arial', 15, 'bold'))
to_currency_label = tk.Label(root, text='Moeda de Destino:', bg="#202630", fg="white", font=('Arial', 15, 'bold'))
amount_label = tk.Label(root, text='Valor:', bg="#202630", fg="white", font=('Arial', 15, 'bold'))
result_label = tk.Label(root, text='Resultado:', bg="#202630", fg="white", font=('Arial', 15, 'bold'))

from_currency_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
to_currency_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
amount_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
result_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="w")

# Dropdown list
from_currency_variable = tk.StringVar()
to_currency_variable = tk.StringVar()

from_currency_menu = ttk.Combobox(root, textvariable=from_currency_variable, values=currency_list, font=('Arial', 15, 'bold'))
to_currency_menu = ttk.Combobox(root, textvariable=to_currency_variable, values=currency_list, font=('Arial', 15, 'bold'))

from_currency_menu.grid(row=0, column=1, padx=10, pady=5, sticky="w")
to_currency_menu.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Campo de Valor
amount_entry = tk.Entry(root, font=('Arial', 15, 'bold'))
amount_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Botão de conversão
convert_button = tk.Button(root, text='Converter', command=convert_currency, bg="#00BFFF", fg="white", font=('Arial', 15, 'bold'))
convert_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")

root.mainloop()