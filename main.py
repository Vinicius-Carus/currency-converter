import ttkbootstrap as ttk
import requests
import json

def main():
    with open('currencies.csv', 'r') as f:
        codes = f.read()
        code_list = codes.splitlines()

    window = ttk.Window()
    window.title('Titulo')
    window.geometry('400x500')

    first_container = ttk.Frame(window)
    first_container.pack()

    second_container = ttk.Frame(window)
    second_container.pack()

    thirdy_container = ttk.Frame(window)
    thirdy_container.pack()

    fourth_container = ttk.Frame(window)
    fourth_container.pack()

    fifth_container = ttk.Frame(window)
    fifth_container.pack()

    label_title = ttk.Label(first_container, text='Currency converter', font='Calibri 20')
    label_title.pack(pady=10)
    
    label_combo_1 = ttk.Label(second_container, text='Convert', font='Calibri 14')
    label_combo_1.pack()
    currency1 = ttk.StringVar(value='BRL')
    combo_symbols1 = set_combo_symbols(second_container, currency1, code_list)
    combo_symbols1.pack()


    label_combo_2 = ttk.Label(thirdy_container, text='To', font='Calibri 14')
    label_combo_2.pack()
    currency2 = ttk.StringVar(value='USD')
    combo_symbols2 = set_combo_symbols(thirdy_container, currency2, code_list)
    combo_symbols2.pack()

    input_number = ttk.StringVar()
    input_number_field = ttk.Entry(fourth_container, textvariable=input_number)
    input_number_field.pack(pady=10)

    button_convert = ttk.Button(fourth_container, 
                                text='Convert', 
                                command=lambda: convert(input_number, currency1, currency2, converted_number, error), 
                                width=30)
    button_convert.pack(pady=10)
    
    converted_number = ttk.StringVar(value=f"0.00 {currency2.get()}")
    converted_number_text = ttk.Label(fifth_container, textvariable=converted_number, font='Calibri 26', padding=30)
    converted_number_text.pack()

    error = ttk.StringVar()
    error_label = ttk.Label(fifth_container, textvariable=error, foreground='red', padding=20, font='Calibri 14')
    error_label.pack()

    window.mainloop()


def set_combo_symbols(container, currency, code_list):
    combobox = ttk.Combobox(container, textvariable=currency, width=30)
    combobox['values'] = code_list
    combobox['state'] = 'readonly'
    return combobox


def convert(number, convert, to, final_number, error):

    if not number.get().isdigit():
        error.set('Only numbers!!!')
        return

    url = f"http://data.fixer.io/api/latest?access_key=a5fd4593091dbcd95b63cfe3d356655e&format=1&symbols={to.get()},{convert.get()}"
    request = requests.get(url)
    response = json.loads(request.content)

    if response['success']:
        error.set('')
        try:
            currency1 = response['rates'][convert.get()]
        except KeyError:
            error.set(f"The API doesn't have this code : {convert.get()}")
            return
        
        try:
            currency2 = response['rates'][to.get()]
        except KeyError:
            error.set(f"The API doesn't have this code :{to.get()}")
            return 
        
        currency1_value = 1/currency1
        converted_number = currency1_value * currency2
        converted_number_total = converted_number * float(number.get())

        text = str("%.2f" % converted_number_total) + " " + to.get()
        final_number.set(text)
    else:
        error.set(f'Something went wrong with the API :(')
        return

main()