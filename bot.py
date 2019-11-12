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
    searched_enzymes = enzymes.Enzymes_List(message.text)

    if not searched_enzymes.is_search:
        bot.send_message(message.chat.id, "Не нашел реактив с таким айди")
    else:
        message_list = searched_enzymes.prepare_to_send()
        for count, msg in enumerate(message_list):
            print(count)
            inline_keyboard = types.InlineKeyboardMarkup()
            edit_button = types.InlineKeyboardButton('Редактировать', callback_data=f'art{count}')
            inline_keyboard.add(edit_button)
            bot.send_message(message.chat.id, msg, reply_markup=inline_keyboard)


@bot.message_handler(content_types=['text'])
def repeat_all_msg(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    select_id=types.KeyboardButton('Поиск по ID')
    markup.add(select_id)
    bot.send_message(message.chat.id, "Пока что я могу только искать реактивы по айди", reply_markup=markup)


@bot.callback_query_handler(lambda query: query.data[:3] == 'art')
def edit_enzyme(query):
    print(query)


try:
    bot.polling(none_stop=True)
except OSError:
    bot.stop_polling()
    proxy_changer.write_proxy(proxy_changer.get_proxy())

