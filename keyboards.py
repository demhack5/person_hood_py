from telebot import types

GET_ACTION_TEXT = 'получить задачу'

get_action_markup = types.ReplyKeyboardMarkup()
get_action_markup.row(types.KeyboardButton(GET_ACTION_TEXT))
