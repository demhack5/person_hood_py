from datetime import datetime
from demhack.utils import *
from demhack.access_manager import *
import traceback
import os

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    Filters, 
    ConversationHandler
)

from telegram import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ParseMode, 
    Document
)

class ErrorHandler (BasicCommunication):
    def __init__(self, *args, **kwargs):
        self.help_message = ""
        self.description = ""
        self.permissions = 0
        self.callbacks = []
        super().__init__(*args, **kwargs) 

    def execute(self, update, context):
        trace = ''.join(traceback.format_list(traceback.extract_tb(context.error.__traceback__)))
        self.state.logger.error(f"Update:\n{update}\n\nTrace:\n{trace}\nError: {context.error}") 
        try:
            context.bot.send_message(int(ADMIN_ID), "[Unhandled exception]")
            try:
                update.message.reply_text("Ой, кажется была обнаружена ошибка, разработчик оповещён.")
            except Exception as ex:
                self.state.logger.warning(f"Error report was not sent to the user, cause: {ex}")
        except Exception as ex:
            self.state.logger.error(f"Error report was not sent to the admin, cause: {ex}")
            try:
                update.message.reply_text("Ой, кажется была обнаружена ошибка, но не удалось оповестить разработчика. Пожалуйста, свяжитесь с куратором бота.")
            except Exception as ex1:
                self.state.logger.error(f"Nobody got error report!\nCause for admin: {ex}\nCause for user: {ex1}\n")
            

class Help (BasicMessage):
        
    def __init__(self, *args, **kwargs):
        self.help_message = "help"
        self.description = "Получить помощь"
        self.permissions = USER | MANAGER
        super().__init__(*args, **kwargs)

    def execute(self, update, context):
        message = obtain_message(update)
        message.reply_text(self.state.help_texts[self.state.access_manager_obj.get_status(
                                str(update.effective_user.id),
                                str(update.effective_user.username))
                            ],
        parse_mode=ParseMode.MARKDOWN)

class Start (BasicMessage):
        
    def __init__(self, *args, **kwargs):
        self.help_message = "start"
        self.description = "Ваш первый опыт"
        self.permissions = USER | MANAGER
        super().__init__(*args, **kwargs)

    def execute(self, update, context):
        update.message.reply_text("Привет " + HANDUPe + ", вы находитесь в умной базе данных")
        message = obtain_message(update)
        message.reply_text(self.state.help_texts[self.state.access_manager_obj.get_status(
                                str(update.effective_user.id),
                                str(update.effective_user.username))
                            ],
        parse_mode=ParseMode.MARKDOWN)

class GetId (BasicMessage):
        
    def __init__(self, *args, **kwargs):
        self.help_message = "get_id"
        self.description = "Получить свой tg-id"
        self.permissions = USER | MANAGER
        super().__init__(*args, **kwargs)

    def execute(self, update, context):
        self.state.access_manager_obj.get_status(str(update.effective_user.id), str(update.effective_user.username))
        update.message.reply_text(str(update.effective_user.id))

class GetManagers (BasicMessage):
        
    def __init__(self, *args, **kwargs):
        self.help_message = "get_managers"
        self.description = "Получить список менеджеров"
        self.permissions = MANAGER
        super().__init__(*args, **kwargs)

    def execute(self, update, context):
        ret = self.state.access_manager_obj.get_managers()
        s = "Вот они, сверху вниз:\n"
        for x in ret:
            s += "@" + x[1] + " (" + x[0] + ")\n"
        update.message.reply_text(s)
        return BasicDialogue.END

class AddManager (BasicDialogue):

    def __init__(self, *args, **kwargs):
        self.help_message = "add_manager"
        self.description = "Добавить менеджера"
        self.permissions = MANAGER
        self.order = [
            SimpleHelloUnit("Введите его id, или /cancel, если не знаете",
                            entry_message=self.help_message),
            DialogueUnit(self.get_id)
        ]
        super().__init__(*args, **kwargs)

    def get_id(self, update, context):
        try:
            id = int(update.message.text)
        except Exception:
            update.message.reply_text("Введите число - id пользователя Telegram")
            return BasicDialogue.END
        self.state.access_manager_obj.set_status(update.message.text, MANAGER)
        update.message.reply_text("Добавлен " + update.message.text)
        return BasicDialogue.END

class EraseManager (BasicDialogue):

    def __init__(self, *args, **kwargs):
        self.help_message = "erase_manager"
        self.description = "Удалить менеджера"
        self.permissions = MANAGER
        self.order = [
            SimpleHelloUnit("Введите его id, или /cancel, если не знаете",
                            entry_message=self.help_message),
            DialogueUnit(self.get_id)
        ]
        super().__init__(*args, **kwargs)

    def get_id(self, update, context):
        self.state.access_manager_obj.set_status(update.message.text, USER)
        update.message.reply_text("Удалён " + update.message.text)
        return BasicDialogue.END
