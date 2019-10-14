import telebot as tb
import proxy_changer
from telebot import types
import db



# Соединяемся с ботом и убираем многопоточность
proxy = proxy_changer.read_proxy()
tb.apihelper.proxy = {'https': 'https://{}:{}'.format(proxy['ip'], proxy['port'])}
bot = tb.TeleBot('725057513:AAGfO-UaRC6Us_ooF-TxqkP2RlevG-jaRfM')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет')
    print(message.chat.id)


@bot.message_handler(commands=['proxy'])
def send_proxy_info(message):
	proxy_info=proxy_changer.get_proxy_info()
	bot.send_message(message.chat.id, 'Работаю на айпи: {}, город: {}, страна: {}'.format(proxy_info['ip'], proxy_info['city'], proxy_info['country']))

@bot.message_handler(func=lambda message: message.text=='Поиск по id')
def search_id(message):
    id_enzymes = bot.send_message(message.chat.id, "по какому id искать")
    bot.register_next_step_handler(id_enzymes, output_result)

def output_result(message):
	connection, cursor = db.connect_to('enzymes.db')
	cursor.execute("SELECT * FROM enzymes WHERE id=?", (message.text, ))
	output = cursor.fetchall()
	if not output:
		bot.send_message(message.chat.id, "я не нашел")
	else:
		bot.send_message(message.chat.id, f'id: {output[0][0]}, name: {output[0][1]}, count: {output[0][2]}')


@bot.message_handler(content_types=['text'])
def repeat_all_msg(message):
    markup=types.ReplyKeyboardMarkup()
    select_id=types.KeyboardButton('Поиск по id')
    markup.add(select_id)
    bot.send_message(message.chat.id, "hjkl", reply_markup=markup)


try:
    bot.polling(none_stop=True)
except OSError:
    bot.stop_polling()
    proxy_changer.write_proxy(proxy_changer.get_proxy())

