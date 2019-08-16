import telebot as tb
import proxy_changer


# Соединяемся с ботом и убираем многопоточность
proxy = proxy_changer.read_proxy()
tb.apihelper.proxy = {'https': 'https://{}:{}'.format(proxy['ip'], proxy['port'])}
bot = tb.TeleBot('')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет')
    print(message.chat.id)


@bot.message_handler(commands=['proxy'])
def send_proxy_info(message):
	proxy_info=proxy_changer.get_proxy_info()
	bot.send_message(message.chat.id, 'Работаю на айпи: {}, город: {}, страна: {}'.format(proxy_info['ip'], proxy_info['city'], proxy_info['country']))


@bot.message_handler(content_types=['text'])
def repeat_all_msg(message):
    bot.reply_to(message, 'Я пока что умею только так')


try:
    bot.polling(none_stop=True)
except OSError:
    bot.stop_polling()
    proxy_changer.write_proxy(proxy_changer.get_proxy())

