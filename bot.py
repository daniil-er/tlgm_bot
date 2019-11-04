import telebot as tb
import proxy_changer
from telebot import types
import db



# Соединяемся с ботом и убираем многопоточность
proxy = proxy_changer.read_proxy()
tb.apihelper.proxy = {'https': f'https://{proxy["ip"]}:{proxy["port"]}'}
bot = tb.TeleBot('725057513:AAGfO-UaRC6Us_ooF-TxqkP2RlevG-jaRfM')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет')


@bot.message_handler(commands=['proxy'])
def send_proxy_info(message):
	proxy_info=proxy_changer.get_proxy_info()
	bot.send_message(message.chat.id, f'Работаю на айпи: {proxy_info["ip"]}, город: {proxy_info["city"]}, страна: {proxy_info["country"]}')


@bot.message_handler(func=lambda message: message.text=='Поиск по ID')
def select_id(message):
    id_enzymes = bot.send_message(message.chat.id, "По какому айди искать?")
    bot.register_next_step_handler(id_enzymes, output_result)

def output_result(message):
	connection, cursor = db.connect_to('enzymes.db')
	cursor.execute("SELECT * FROM enzymes WHERE id=?", (message.text, ))
	data_enzymes = cursor.fetchall()
	if not data_enzymes:
		bot.send_message(message.chat.id, "Не нашел реактив с таким айди")
	else:
		markup=types.InlineKeyboardMarkup()
		edit_button=types.InlineKeyboardButton('Редактировать', callback_data='edit')
		markup.add(edit_button)
		bot.send_message(message.chat.id, f'id: {data_enzymes[0][0]}, name: {data_enzymes[0][1]}, count: {data_enzymes[0][2]}')


@bot.message_handler(content_types=['text'])
def repeat_all_msg(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    select_id=types.KeyboardButton('Поиск по ID')
    markup.add(select_id)
    bot.send_message(message.chat.id, "Пока что я могу только искать реактивы по айди", reply_markup=markup)


@bot.callback_query_handler(lambda query: True)
def press_button(query):
	if query.data == 'edit':
		bot.send_message(query.message.chat.id, "сколько реактивов осталось?")
	else:
		pass

try:
    bot.polling(none_stop=True)
except OSError:
    bot.stop_polling()
    proxy_changer.write_proxy(proxy_changer.get_proxy())

