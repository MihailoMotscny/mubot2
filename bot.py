import telebot
import pickle
from telebot import types
from telebot.types import InlineKeyboardMarkup
from google_sheets import sheet_adding, GoogleSheet
from datetime import datetime

TOKEN = '6793483259:AAH9N2QG8HcWJiq4whlYRXPvXWL0WzcfDrA'
bot = telebot.TeleBot(TOKEN)


class Bot():
    # number_string = {'А95': 8, 'д.т.': 41, '15w40': 5, 'ТурбоДизель': 2}
    # drivers = ["Моцний Михайло Олексійович"]
    # cars = ["Джон Дір 30725", "Джон Дір 30724"]
    # past_indicator = {'МТЗ 25803': 12586, 'Форд 0219': 385733}
    # combains = ['Лексіон 34343', 'Лексіон б.н.']
    # fuel = ["А95", "д.т.", "15w40", "ТурбоДизель"]
    speed_counter_cars = []
    #
    # with open('combails.pickle', 'wb') as file:
    #     pickle.dump(combains, file)

    # with open('drivers.pickle', 'wb') as file:
    #     pickle.dump(drivers, file)
    #
    # with open('data.pickle', 'wb') as file:
    #     pickle.dump(number_string, file)
    #
    # with open('fuel.pickle', 'wb') as file:
    #     pickle.dump(fuel, file)
    with open('drivers.pickle', 'rb') as file:
        drivers = pickle.load(file)
    with open('data.pickle', 'rb') as file:
        number_string = pickle.load(file)
        print(number_string)

    with open('cars.pickle', 'rb') as file:
        cars = pickle.load(file)
        print(cars)

    with open('fuel.pickle', 'rb') as file:
        fuel = pickle.load(file)
    print(fuel)

    with open('indicators.pickle', 'rb') as file:
        past_indicator = pickle.load(file)
    print(past_indicator)

    with open('combails.pickle', 'rb') as file:
        combains = pickle.load(file)
    print(combains)

    counter = 0
    plomba_num = 0
    indicator = 0
    fuel_value = 0
    data = {}

    colum_title_index = 0

    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        addingRecordButton = types.KeyboardButton('Додати запис')
        viewRecords = types.KeyboardButton('/start')
        uppdateRecords = types.KeyboardButton('Редагувати запис')
        makeReport = types.KeyboardButton('Додати комбайн')
        addPosition = types.KeyboardButton('Додати позицію')

        markup.add(addingRecordButton, viewRecords, uppdateRecords, makeReport, addPosition)
        bot.send_message(message.chat.id, f"Привіт,{message.from_user.first_name}", reply_markup=markup)
        global chat_id
        chat_id = message.chat.id
        print(chat_id)

    @bot.message_handler(content_types=['text'])
    def controller(message):
        if message.text == 'Додати запис':
            print('Додати запис')
            Bot.driver(message)
        if message.text == 'Додати позицію':
            Bot.addPosition(message)
            print('Додати позицію')

    @bot.message_handler(content_types=['text'])
    def reports(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Створити звіт за місяць')
        button2 = types.KeyboardButton('Створити звіт з фільтрами')

        markup.add(button1, button2)
        bot.send_message(chat_id, 'Обери тип звіту', reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def reports(message):
        if message.text == 'Створити звіт за місяць':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton('Створити звіт за місяць')
            button2 = types.KeyboardButton('Створити звіт з фільтрами')

            markup.add(button1, button2)
            bot.send_message(chat_id, 'Обери тип звіту', reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def addPosition(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Додати рідину')
        button2 = types.KeyboardButton('Додати авто')
        button3 = types.KeyboardButton('Додати водія')
        button4 = types.KeyboardButton('Додати комбайн')
        button5 = types.KeyboardButton('/start')
        send = bot.send_message(chat_id, "Ок")

        markup.add(button1, button2, button3, button4, button5)
        bot.send_message(chat_id, 'Обери тип звіту', reply_markup=markup)
        bot.register_next_step_handler(send, Bot.type_controller)

    lastmessage = ''

    def type_controller(message):

        Bot.lastmessage = message.text
        if message.text == "Додати рідину":
            send = bot.send_message(chat_id, "Введіть назву рідини:")
        if message.text == "Додати авто":
            send = bot.send_message(chat_id, "Введіть назву авто:")
        if message.text == "Додати водія":
            send = bot.send_message(chat_id, "Введіть ПІБ:")
        if message.text == "Додати комбайн":
            send = bot.send_message(chat_id, "Введіть назву комбайна:")
        if message.text == "/start":
            send = bot.send_message(chat_id, "/start")
        bot.register_next_step_handler(send, Bot.adding_new_type_of)

    def adding_new_type_of(message):
        if Bot.lastmessage == "Додати рідину":
            Bot.fuel.append(message.text)
            gs = GoogleSheet()
            gs.add_nylist(message.text)
            Bot.number_string[message.text] = 2
            sheet_adding(message.text, 1, 1, "Прізвище та ініціали", "Марка автомобіля", "Кількість пального",
                         "Номер пломби", "Дата та час")
            with open('fuel.pickle', 'wb') as file:
                pickle.dump(Bot.fuel, file)

        if Bot.lastmessage == "Додати авто":
            Bot.cars.append(message.text)
            with open('cars.pickle', 'wb') as file:
                pickle.dump(Bot.cars, file)

        if Bot.lastmessage == "Додати водія":
            Bot.drivers.append(message.text)
            with open('drivers.pickle', 'wb') as file:
                pickle.dump(Bot.drivers, file)

        if Bot.lastmessage == "Додати комбайн":
            Bot.combains.append(message.text)
            with open('combails.pickle', 'wb') as file:
                pickle.dump(Bot.combains, file)

        Bot.start(message)

    @bot.message_handler(content_types=['text'])
    def driver(self):
        button_dic = {}
        markup = InlineKeyboardMarkup()

        for elem in Bot.drivers:
            button = types.InlineKeyboardButton(elem, callback_data=elem)
            markup.add(button)

        bot.send_message(chat_id, text="Обери водія", reply_markup=markup)

    def car(self):
        markup = InlineKeyboardMarkup()
        for elem in Bot.cars:
            button = types.InlineKeyboardButton(elem, callback_data=elem)
            markup.add(button)
            print(markup)

        bot.send_message(chat_id, text="Обери автомобіль", reply_markup=markup)

    def fuel_name(self):
        markup = InlineKeyboardMarkup()

        for elem in Bot.fuel:
            button = types.InlineKeyboardButton(elem, callback_data=elem)
            markup.add(button)

        bot.send_message(chat_id, text="Обери рідину", reply_markup=markup)

    def fuel_value_func(self):
        send = bot.send_message(chat_id, "Введіть літри:")
        bot.register_next_step_handler(send, Bot.value)

    def value(message):
        Bot.fuel_value = message.text
        Bot.counter += 1
        print(Bot.fuel_value)
        send = bot.send_message(chat_id, 'Введіть номер пломби:')
        bot.register_next_step_handler(send, Bot.plomba)

    def plomba(message):
        Bot.plomba_num = message.text
        send = bot.send_message(chat_id, 'Введіть показник пробігу:')
        bot.register_next_step_handler(send, Bot.new_indicator)

    def new_indicator(message):
        Bot.indicator = message.text
        FuelName = 'FuelName'
        print(Bot.plomba_num)
        data_time_formate = datetime.now()
        last_indicator = 0
        print(f"Те шо нада {Bot.number_string[Bot.data['FuelName']]}")
        new_indicator = 1
        if Bot.data['CarName'] in Bot.past_indicator and (Bot.data["FuelName"] == 'д.т.' or Bot.data[
            "FuelName"] == 'А95'):

            last_indicator = Bot.past_indicator[Bot.data['CarName']]
            Bot.past_indicator[Bot.data['CarName']] = Bot.indicator
            new_indicator = Bot.indicator
        else:
            if Bot.data["FuelName"] == 'д.т.' or Bot.data[
                "FuelName"] == 'А95':
                Bot.past_indicator[Bot.data['CarName']] = Bot.indicator
                last_indicator = 1
                new_indicator = Bot.indicator

            else:
                new_indicator = 1
                last_indicator = 1
                print(Bot.past_indicator[Bot.data['CarName']])

        with open('indicators.pickle', 'wb') as file:
            pickle.dump(Bot.past_indicator, file)

        difference = int(new_indicator) - int(last_indicator)
        if difference == 0 or Bot.data['CarName'] in Bot.combains:
            difference = 1

        consumption = 0
        if Bot.data['CarName'] in Bot.combains:
            consumption = float(Bot.fuel_value) / Bot.indicator

        else:
            consumption = (float(Bot.fuel_value) / difference) * 100

        sheet_adding(Bot.data['FuelName'],

                     Bot.number_string[Bot.data['FuelName']],
                     Bot.number_string[Bot.data['FuelName']],
                     Bot.data['DriverName'],
                     Bot.data['CarName'], Bot.fuel_value, Bot.plomba_num,
                     str(data_time_formate.strftime("%Y-%m-%d %H:%M")), last_indicator,
                     new_indicator, difference, consumption)

        bot.send_message(chat_id, 'Запис додано👍')
        bot.send_message(chat_id, 'Водій: ' + str(Bot.data['DriverName']))
        bot.send_message(chat_id, 'Автомобіль: ' + str(Bot.data['CarName']))
        bot.send_message(chat_id, 'Назва рідини: ' + str(Bot.data['FuelName']))
        bot.send_message(chat_id, 'Кількість пального: ' + str(Bot.fuel_value))
        bot.send_message(chat_id, 'Номер пломби: ' + str(Bot.plomba_num))
        bot.send_message(chat_id, 'Старий показник: ' + str(last_indicator))
        bot.send_message(chat_id, 'Новий показник: ' + str(new_indicator))
        bot.send_message(chat_id, 'Проїхано: ' + str(difference) + " км")
        bot.send_message(chat_id, 'Розход: ' + str(consumption) + " л/100км")

        Bot.counter = 0
        Bot.number_string[Bot.data[FuelName]] += 1

        with open('data.pickle', 'wb') as file:
            pickle.dump(Bot.number_string, file)

    @bot.callback_query_handler(func=lambda call: call.data)
    def post_for_gh(call):
        global drivers, cars, fuel
        print(call.data)
        if call.data in Bot.drivers:
            Bot.data['DriverName'] = str(call.data)
            Bot.car(call)
            Bot.counter += 1
            print(Bot.data)
        if call.data in Bot.cars:
            Bot.data['CarName'] = str(call.data)
            Bot.fuel_name(call)
            Bot.counter += 1
            print(Bot.data)

        if call.data in Bot.fuel:
            Bot.data['FuelName'] = str(call.data)
            print(f"Те шо нада {Bot.number_string[Bot.data['FuelName']]}")
            print(Bot.data)
            Bot.counter += 1

        if Bot.counter >= 3:
            Bot.fuel_value_func(call)


bot.infinity_polling()
