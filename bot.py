import telebot as tb
import proxy_changer
from telebot import types
import db
import enzymes



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
	search_result = enzymes.Enzymes_List(message.text)
	if not search_result.is_search:
		bot.send_message(message.chat.id, "Не нашел реактив с таким айди")
	else:
		keyboard_edit=types.InlineKeyboardMarkup()
		edit_button=types.InlineKeyboardButton('Редактировать', callback_data='edit')
		keyboard_edit.add(edit_button)
		bot.send_message(message.chat.id, f'{search_result.get_list_enzymes()}', reply_markup = keyboard_edit)


@bot.message_handler(content_types=['text'])
def repeat_all_msg(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    select_id=types.KeyboardButton('Поиск по ID')
    markup.add(select_id)
    bot.send_message(message.chat.id, "Пока что я могу только искать реактивы по айди", reply_markup=markup)


@bot.callback_query_handler(lambda query: True)
def press_button(query):
	if query.data == 'edit':
		data_enz = bot.send_message(query.message.chat.id, "Сколько взяли?")
		bot.register_next_step_handler(data_enz, enzymes_edit)
	else:
		pass


def enzymes_edit(message):
	src = message.text.split('-')
	enzymes_data = {src[0]: src[1]}
	print(enzymes_data)

try:
    bot.polling(none_stop=True)
except OSError:
    bot.stop_polling()
    proxy_changer.write_proxy(proxy_changer.get_proxy())

