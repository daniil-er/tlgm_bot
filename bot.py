import telebot as tb
import proxy_changer
from telebot import types
import db
import enzymes



# Соединяемся с ботом и убираем многопоточность
proxy = proxy_changer.read_proxy()
tb.apihelper.proxy = {'https': f'https://{proxy["ip"]}:{proxy["port"]}'}
bot = tb.TeleBot('725057513:AAGfO-UaRC6Us_ooF-TxqkP2RlevG-jaRfM')
enzymes_storage = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	button_search_enzymes = types.KeyboardButton('Поиск реактива')
	keyboard.add(button_search_enzymes)
	bot.send_message(message.chat.id, f'Привет, {message.chat.first_name}.\nЧтобы найти данные по реактиву нажми на кнопку или отправь мне его название',
					 reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Поиск реактива')
def get_name_enzymes(message):
    id_enzymes = bot.send_message(message.chat.id, "По какому названию искать?")
    bot.register_next_step_handler(id_enzymes, output_searched_enzymes)

def output_searched_enzymes(message):
	searched_enzymes = enzymes.Enzymes_List(message.text)
	enzymes_storage[message.chat.id] = searched_enzymes
	if not searched_enzymes.is_search:
		bot.send_message(message.chat.id, "Не нашёл реактив с таким названием")
	else:
		keyboard_edit=types.InlineKeyboardMarkup()
		edit_button=types.InlineKeyboardButton('Редактировать', callback_data='edit')
		keyboard_edit.add(edit_button)
		bot.send_message(message.chat.id, f'{searched_enzymes.get_list_enzymes()}', reply_markup=keyboard_edit)


@bot.message_handler(content_types=['text'])
def repeat_all_msg(message):
    output_searched_enzymes(message)


@bot.callback_query_handler(lambda query: True)
def pressed_button(query):
	if query.data == 'edit':
		data_on_made_enzymes = bot.send_message(query.message.chat.id, "Сколько взяли?\nНапишите в формате <b>количество_реактива-объём_реактива</b>, например: <b>2-s</b>",
												parse_mode='html')
		bot.register_next_step_handler(data_on_made_enzymes, enzymes_edit)
	else:
		pass

def enzymes_edit(message):
	enzymes_amount, enzymes_volume = message.text.split('-')
	user_enzymes_list= enzymes_storage[message.chat.id]
	if user_enzymes_list.edit_enzymes(enzymes_amount, enzymes_volume):
		bot.send_message(message.chat.id, 'Обновил информацию в базе')
	else:
		bot.send_message(message.chat.id, 'Не получилось обновить информацию.\nСкорее всего проблема с форматированием данных реактива, поправьте их в базе')


try:
    bot.polling(none_stop=True)
except OSError:
    bot.stop_polling()
    proxy_changer.write_proxy(proxy_changer.get_proxy())
