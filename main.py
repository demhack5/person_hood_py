import telebot

from keyboards  import *
from users_data import *

TOKEN = open('TOKEN.txt').read()
bot = telebot.TeleBot(TOKEN)

init_table()
# id корневого квеста
ROOT_ID = 10000

ROOT_USER_ID = ...

def get_registration_link(user_id):
    return "https:://registrate"

@bot.message_handler(commands=['start', 'begin'])
def start_handler(msg):

    user_id = msg.from_user.id
    bot.send_message(user_id, "Приветствую, выполните следующие действия перед тем как получите ссылку на регистрацию!", reply_markup=get_action_markup)

@bot.message_handler()
def text_handler(msg):

    user_id = msg.from_user.id

    check_user_in_database(user_id)
    if msg.text == GET_ACTION_TEXT:
        
        msg_text = ""

        if validate_last_action(user_id):
            if get_cur_stage(user_id) == N_STAGES - 1:
                msg_text = "Прекрасно! Теперь ты можешь зарегистироваться на наш ресурс %s" % (get_registration_link(user_id))
                bot.send_message(user_id, text = msg_text)
            else:
                msg_text = get_next_action_text(user_id)
                bot.send_message(user_id, text = msg_text, reply_markup = get_action_markup)
        else:
            msg_text = "Валидация провалена, повторите\n\n" + get_next_action_text
            bot.send_message(user_id, text = msg_text, reply_markup = get_action_markup)

    return

print('connecting')
bot.polling()
