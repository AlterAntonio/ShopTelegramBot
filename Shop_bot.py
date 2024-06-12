import telebot

bot = telebot.TeleBot('ТУТ_БЫЛ_ТОКЕН')

shop_list = ['Текущий список покупок:']

help = ['Чтобы добавить пункт в список, просто отправь его как сообщение', 'Вот доступные команды:', '/start - приветствие', '/help - это там где ты сейчас',
        '/shop - покажет список из введённых сообщений', '/title - после этой команды можно ввести заголовок списка',
        '/0 - вместо нуля надо ввести номер по списку, а затем наименование - так ы поменяешь этот пункт.'
        ' Если команду так и оставить просто с номером - пункт с этим номером будет удалён']
def show_list(shop_list):
    if len(shop_list) > 1:
        show_list = [shop_list[0]]
        for index, item in enumerate(shop_list[1:], 1):
            show_list.append(f'{index} - {item}')
        return '\n'.join(show_list)
    else: return f'{shop_list[0]}\nСписок пуст'

@bot.message_handler(commands=['start', 'help'])
def start_help(message):
    if message.text == '/start':
        bot.reply_to(message, 'Привет! Я помогу тебе составить список, покупок например. Этот список будет '
                              'состоять из твоих сообщений. Просмотреть его можно по команде /shop, чтобы посмотреть '
                              'другие команды - жми /help')
    elif message.text == '/help':
        bot.reply_to(message, '\n'.join(help))

@bot.message_handler(commands=['shop'])
def echo_messages(message):
    bot.reply_to(message, show_list(shop_list))

@bot.message_handler(commands=['title'])
@bot.edited_message_handler(func=lambda message: message.text.startswith('/title'))
def title(message):
    global shop_list
    if len(message.text) > 7:
        shop_list[0] = message.text[7:]
        bot.reply_to(message, f'Заголовок изменён на {shop_list[0]}')
    elif len(message.text) <= 7:
        bot.reply_to(message, 'Укажите новый заголовок после команды "/title "')

@bot.message_handler(func=lambda message: message.text.startswith('/'))
def edit_shop_list(message):
    value = message.text[1:].split(' ', 1)
    if len(shop_list) > 1 and value[0].isdecimal():
        if 1 <= int(value[0]) < len(shop_list):
            index = int(value[0])
            if len(value) == 2:
                new_value = value[1]
                bot.reply_to(message, f'"{shop_list[index]}" заменён на "{new_value}"')
                shop_list[index] = new_value
                bot.reply_to(message, show_list(shop_list))
            elif len(value) == 1:
                pop_value = shop_list.pop(index)
                bot.reply_to(message, f'Пункт "{pop_value}" удалён из списка!\n{show_list(shop_list)}')
    elif len(shop_list) > 1 and value[0].isdecimal():
        bot.reply_to(message, 'Список пуст, нечего менять!')

@bot.message_handler(func=lambda message: True)
def save_message(message):
    shop_list.append(message.text)
    bot.reply_to(message, "Добавлено!")

# Запуск бота
bot.polling()