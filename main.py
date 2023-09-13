import telebot
import config
import db

bot = telebot.TeleBot(config.TOKEN)

start_text = """Привет!

Есть две команды, /income и /outcome

В каждой из команд есть свои котегории, увидите если введете в чат
"""

income_text = """Выберите категорию доходов:

{}

Если хотите добавить новую категорию просто напишите это в формате category - описание. 
Пример: taxi - доходы в такси
"""

outcome_text = """Выберите категорию расходов:

{}

Если хотите добавить новую категорию просто напишите это в формате category - описание. 
Пример: taxi - расходы на такси
"""

category = ""
summ = 0
comment = ""
incfl   = 0


@bot.message_handler(content_types=['text'])
def start(message):
    db.check_user(message.from_user.id, f'{message.from_user.first_name} {message.from_user.last_name}',
                  message.from_user.username)
    global incfl
    if message.text == '/start':
        global start_text
        bot.send_message(message.from_user.id, start_text)
    elif message.text == '/income':
        incfl=1
        ctgrs = ""
        for i, j in enumerate(db.get_ctg(message.from_user.id, 1)):
            ctgrs = f'{ctgrs}{i}) /{j[0]} - {j[1]}\n'
        global income_text
        bot.send_message(message.from_user.id, income_text.replace('{}', ctgrs))
        bot.register_next_step_handler(message, get_category)
    elif message.text == '/outcome':
        incfl = 0
        ctgrs = ""
        for i, j in enumerate(db.get_ctg(message.from_user.id, 0)):
            ctgrs = f'{ctgrs}{i}) /{j[0]} - {j[1]}\n'
        global outcome_text
        bot.send_message(message.from_user.id, outcome_text.replace('{}', ctgrs))
        bot.register_next_step_handler(message, get_category)


def get_category(message):
    global category
    category = message.text
    bot.send_message(message.from_user.id, 'Введите сумму')
    bot.register_next_step_handler(message, get_summ)


def get_summ(message):
    global summ
    summ = float(message.text.strip())
    bot.send_message(message.from_user.id, 'Ваши комментарии?')
    bot.register_next_step_handler(message, get_comm)


def get_comm(message):
    global comment
    comment = message.text.strip()
    db.add_operation(message.from_user.id, category,summ,comment,incfl)
    bot.send_message(message.from_user.id, 'Операция сохранена!')


bot.polling(none_stop=True, interval=0)
