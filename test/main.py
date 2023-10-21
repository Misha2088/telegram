import types
from telebot import types
from PIL import Image
import telebot
import sqlite3

bot = telebot.TeleBot('6713837229:AAEXyNIwL5m3-idVP4lnhbgv5OgZ8tc_rkE')
name = ''

print('kejf')


print('fsifjwofjqpjwfwfpwnfpwfw')
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('/поиск')
    btn2 = types.KeyboardButton('/новая_заявка')
    btn3 = types.KeyboardButton('/Удалить_заявку')
    markup.add(btn1,btn2, btn3)
    mess = 'Здравствуйте, я - бот помощник, созданный для упрщения ведения бизнеса.\nЧем могу помочь?'
    bot.send_message(message.chat.id, mess, reply_markup=markup)

@bot.message_handler(commands=["Новая_заявка", "новая_заявка"])
def new_anket(message):
    conn = sqlite3.connect('itproger.sqlite3')  # Открыть БД
    cur = conn.cursor()  # Открыть БД

    cur.execute('''CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key,  
        numberOfOrder varchar(100) , 
        userName varchar(100), 
        telephoneNumber varchar(100),
        adress varchar(45), 
        service varchar(45), 
        cost varchar(100), 
        timeOfEntrance varchar(100),
        timeOfWork varchar(100),
        masterName varchar(100),
        shopName varchar(45),
        status varchar(45),
        buyStatus varchar(45),
        comment varchar(300))''')  # Create Table_name

    #cur.execute('''CREATE UNIQUE INDEX 'uniq' ON 'users'('numberOfOrder')''')
    conn.commit()
    cur.close()  # Close DB
    conn.close()

    bot.send_message(message.chat.id, 'Введите номер заказа.')
    bot.register_next_step_handler(message, def_numberOfOrder)  # Отправление в следующий хендлер

@bot.message_handler(commands=['поиск','Поиск'])
def search(message):
    bot.send_message(message.chat.id, 'Введите номер заявки')
    bot.register_next_step_handler(message, search_2)  # Отправление в следующий хендлер


def search_2(message):
    global numberOfOrder
    numberOfOrder = message.text.strip()
    bot.send_message(message.chat.id, f'Заявка номер: {numberOfOrder}\nЕсли нет ифнормации по номеру заявки - заявка отстуствует в базе данных!')

    conn = sqlite3.connect('itproger.sqlite3')
    cur = conn.execute('''SELECT * FROM users WHERE numberOfOrder= ?''', (numberOfOrder,))

    info = ''  # Прогонка всех столбцов троки
    kat = ['Номер заявки', 'ФИО клиента', 'Номер телефона', 'Адрес', 'Услуга', 'Стоимость', 'Время поступление', 'Дата работы', 'ФИО мастера', 'Магазин', 'Статус', 'Статус оплаты', 'Комментарий', '']
    for el in cur:
        for i in range(1, 13):
            info += f'{kat[i-1]}: {el[i]}\n'
        print('')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, info)

@bot.message_handler(commands=['Удалить_заявку','удалить_заявку'])
def delete_all(message):
    bot.send_message(message.chat.id, 'Введите номер заявки')
    bot.register_next_step_handler(message, delete_all_2) #Отправление в следующий хендлер


def delete_all_2(message):
    numberOfOrder = message.text.strip()
    mess = f'Вы удалили заявку номер: {numberOfOrder}!\n'
    bot.send_message(message.chat.id, mess)

    conn = sqlite3.connect('itproger.sqlite3')
    cur = conn.execute('''DELETE FROM users WHERE numberOfOrder= ?''', (numberOfOrder,))

    conn.commit()
    cur.close()
    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('/поиск')
    btn2 = types.KeyboardButton('/новая_заявка')
    btn3 = types.KeyboardButton('/Удалить_заявку')
    markup.add(btn1, btn2, btn3)



@bot.message_handler(commands=['delete'])
def delete(message):
    conn = sqlite3.connect('itproger.sqlite3')
    cur = conn.cursor()

    cur.execute('''DELETE FROM users''')  # Очистка БД
    conn.commit()
    cur.close()
    conn.close()


def def_numberOfOrder(message):
    global numberOfOrder
    global temp
    numberOfOrder = message.text.strip()
    temp=numberOfOrder
    bot.send_message(message.chat.id, 'Введите ФИО клиента')
    bot.register_next_step_handler(message, def_userName)


def def_userName(message):
    global userName
    userName = message.text.strip()
    bot.send_message(message.chat.id, 'Введите номер телефона')
    bot.register_next_step_handler(message, def_telephoneNumber)


def def_telephoneNumber(message):
    global telephoneNumber
    telephoneNumber = message.text.strip()
    bot.send_message(message.chat.id, 'Введите адрес')
    bot.register_next_step_handler(message, def_adress)


def def_adress(message):
    global adress
    adress = message.text.strip()
    bot.send_message(message.chat.id, 'Введите услугу')
    bot.register_next_step_handler(message, def_service)


def def_service(message):
    global service
    service = message.text.strip()
    bot.send_message(message.chat.id, 'Введите стоимость')
    bot.register_next_step_handler(message, def_cost)


def def_cost(message):
    global cost
    cost = message.text.strip()
    bot.send_message(message.chat.id, 'Введите дату и время поступления')
    bot.register_next_step_handler(message, def_timeOfEntrance)


def def_timeOfEntrance(message):
    global timeOfEntrance
    timeOfEntrance = message.text.strip()
    bot.send_message(message.chat.id, 'Введите дату и время работы')
    bot.register_next_step_handler(message, def_timeOfWork)


def def_timeOfWork(message):
    global timeOfWork
    timeOfWork = message.text.strip()
    bot.send_message(message.chat.id, 'Введите ФИО мастера')
    bot.register_next_step_handler(message, def_masterName)


def def_masterName(message):
    global masterName
    masterName = message.text.strip()
    bot.send_message(message.chat.id, 'Введите название магазина')
    bot.register_next_step_handler(message, def_shopName)


def def_shopName(message):
    global shopName
    shopName = message.text.strip()
    bot.send_message(message.chat.id, 'Введите статус')
    bot.register_next_step_handler(message, def_status)


def def_status(message):
    global status
    status = message.text.strip()
    bot.send_message(message.chat.id, 'Введите статус оплаты')
    bot.register_next_step_handler(message, def_buyStatus)


def def_buyStatus(message):
    global buyStatus
    buyStatus = message.text.strip()
    bot.send_message(message.chat.id, 'Введите комментарий')
    bot.register_next_step_handler(message, def_comment)


def def_comment(message):
    global comment
    comment = message.text.strip()
    conn = sqlite3.connect('itproger.sqlite3')
    cur = conn.cursor()

    # Занесение переменных в БД
    cur.execute('''INSERT INTO users (numberOfOrder, 
            userName, 
            telephoneNumber, 
            adress, 
            service, 
            cost, 
            timeOfEntrance, 
            timeOfWork, 
            masterName, 
            shopName, 
            status, 
            buyStatus, 
            comment) 
            VALUES 
            ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")''' % (
        numberOfOrder, userName, telephoneNumber, adress, service, cost, timeOfEntrance, timeOfWork, masterName,
        shopName, status, buyStatus, comment))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Проверить заявку', callback_data='users'))
    bot.send_message(message.chat.id, 'Проверка', reply_markup=markup)




@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('itproger.sqlite3')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users ORDER BY id DESC LIMIT 1')
    users = cur.fetchall()

    info = ''  # Прогонка всех столбцов троки
    kat = ['Номер заявки', 'ФИО клиента', 'Номер телефона', 'Адрес', 'Услуга', 'Стоимость', 'Время поступление',
           'Дата работы', 'ФИО мастера', 'Магазин', 'Статус', 'Статус оплаты', 'Комментарий' ]
    for el in users:
        for i in range(1, 13):
            info += f'{kat[i - 1]}: {el[i]}\n'
        print('')

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)

@bot.message_handler(commands=['Удалить_эту_заявку', 'удалить_эту_заявку'])
def deleteThis(message):
    global temp
    mess = f'Вы удалили только что созданную заявку: {temp}'
    bot.send_message(message.chat.id, mess)

    conn = sqlite3.connect('itproger.sqlite3')
    cur = conn.execute('''DELETE FROM users WHERE numberOfOrder= ?''', (temp,))

    conn.commit()
    cur.close()
    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('/поиск')
    btn2 = types.KeyboardButton('/новая_заявка')
    btn3 = types.KeyboardButton('/Удалить_заявку')
    btn4 = types.KeyboardButton('/Удалить_эту_заявку')
    markup.add(btn1, btn2, btn3, btn4)

bot.polling(none_stop=True)