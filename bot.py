from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.error import BadRequest, Unauthorized
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, Updater)
from telegram.utils.helpers import effective_message_type

import threading
from time import sleep
from sqlcommand import DB
##########-> INFO BOT AND CREATE DATABASE <-##########

username_admin = "@ad_vdporn"
id_admin = (1904100632,1704934550)
db= DB("botSellFile.bak")
db.table()
token = "2125398599:AAHLSPAVk8Ig-HtL__z8uT7Us5r4AjMw4QI"
updater = Updater(token)
disp = updater.dispatcher
id_channel="\n channel bot => @vdporn "

##########-> SATRT BOT COMMANDS <-##########

def start(update: Update, context: CallbackContext  , text_admin:str= None):
    db.insert_user(update.effective_user.id)
    text = update.message.text
    if text_admin:
        text = text_admin
    if text :
        button = [["خرید"],["راهنما"]]
        update.message.reply_text("سلام کاربر گرامی به ربات ما خوش آمدید.\nلطفا از دکمه ها استفاده کنید.",
                                reply_markup=ReplyKeyboardMarkup(button,resize_keyboard=True))

START_ADMIN_MODE, GET_NAME_FILE, GET_FILE , SENDALL ,ADD_USER , USER_ID ,  name= range(7)

def adminam(update: Update, context: CallbackContext):
    if update.effective_chat.id in id_admin:
        key = [["ارسال فایل" ,"دریافت لیست کاربران"],
              ["ارسال پیام به همه", "اضافه کردن کاربر"],["دریافت لیست فایل ها"],["برگشت به صفحه اصلی"]]
        update.message.reply_text("سلام مدیر خوش امدید",
                                  reply_markup=ReplyKeyboardMarkup(key, resize_keyboard=True))
        return START_ADMIN_MODE
    else:
        update.message.reply_text("شما مدیر ربات نیستید")

def cancel(update: Update, context: CallbackContext):
    user = update.effective_user.id
    update.message.reply_text("به صفحه اصلی برگشتید.")
    start(update, context , text_admin=  "start")
    return ConversationHandler.END


def start_panel_admin(update: Update, context: CallbackContext):
    text = update.message.text

    if text =="ارسال فایل":
        if update.effective_user.id in id_admin:
            update.message.reply_text("لطفا نام فایل ها را ارسال کنید: ")
            return GET_NAME_FILE

    elif text == "دریافت لیست کاربران":
        if update.effective_user.id in id_admin:
            info_users = db.get_users()
            msg = "لیست کاربران شما به شرح زیر است:\n"
            for user in info_users:
                msg = msg + f"\n {user[0]} ==> {user[1]}"
            update.message.reply_text(msg)

    elif text == "ارسال پیام به همه":
        update.message.reply_text("پیامی که میخواهید به همه ارسال شود را بفرستید\nشما میتوانید با دسستور\n /cancel\n از حالت خارج شوید",
                                  reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        return SENDALL

    elif text == "اضافه کردن کاربر":
        update.message.reply_text("ایدی عددی و مقداری  کسی که میخواهید اضافه کنید را بفرستید :\n برای مثال: \n 111111111,5000 ")
        return ADD_USER

    elif text == "دریافت لیست فایل ها":
        if update.effective_user.id in id_admin:
            info_users = db.get_file_number()
            msg = "لیست فایل های شما به شرح زیر است:\n"
            for file in info_users:
                msg = msg + f"\n {file[0]} ==> {file[1]}"
            update.message.reply_text(msg)

    elif text == "برگشت به صفحه اصلی":
        cancel(update, context)

    else:
        update.message.reply_text("از دکمه ها استفاده کنید.")

def get_name_file(update: Update, context: CallbackContext):
    if update.effective_user.id in id_admin:
        global name
        name = update.message.text
        update.message.reply_text("حالا فایل های مربوطه رو ارسال کنید در صورت اتمام فایل ها از\n /cancel \n استفاده کنید",
                                  reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        return GET_FILE

def add_user(update: Update, context: CallbackContext):
    text = update.effective_message.text
    info = text.split(",")
    try:
        db.update_user(info[0],int(info[1]))
    except:
        update.message.reply_text("کاربر در ربات عضو نیست!")
        return START_ADMIN_MODE
    update.message.reply_text("کاربر اضافه شد")
    context.bot.send_message(info[0] , "ربات برای شما فعال شد")
    return START_ADMIN_MODE

def get_input_file(update: Update, context: CallbackContext):
    if update.effective_user.id in id_admin:
        type_message = effective_message_type(update)
        if type_message == 'video':
            file_id = update.message.video.file_id
        elif type_message == 'photo':
            file_id = update.message.photo[0].file_id
        elif type_message == 'document':
            file_id = update.message.document.file_id
        elif type_message == 'video_note':
            file_id = update.message.video_note.file_id
        elif type_message == 'voice':
            file_id = update.message.voice.file_id
        elif type_message == 'audio':
            file_id = update.message.audio.file_id
        db.insert_file(name , file_id , type_message)
        return GET_FILE

def send_all(update: Update, context: CallbackContext):
    text = update.effective_message.text
    count, list_users = 0, db.get_users()
    if text == '/cancel':
        return cancel(update, context)
    for user in list_users:
        try:
            context.bot.send_message(text=text, chat_id=user[0])
            count += 1
        except(Unauthorized, BadRequest):
            pass
    update.message.reply_text("پیام مورد نظر به کاربر ها ارسال شد")
    return ConversationHandler.END


def hellp(update: Update, context:CallbackContext ):
    numfile = db.get_users(update.effective_user.id)
    msg = f"""
برای دریافت فایل از دستور زیر استفاده کنید
/myfile num
بعد دستور یک فاصله قرار دهید و تعداد فایل را ذکر کنید
شما تعداد {numfile} فایل خریده اید
پس اعداد بین 1 تا {numfile} را وارد کنیئ

مرسی از خرید شما :)
"""
    if db.get_users(update.effective_user.id)[0] is not None:
        update.message.reply_text(msg)
    else:
        update.message.reply_text("این بخش مربوط به روش دریافت فایل هست\nچون شما خرید نکرده اید برای شما نمایش داده نمیشه.")

def sell(update: Update, context:CallbackContext):
    msg = f"""
سلام جهت خرید به ایدی زیر پیام بدید
{username_admin}
"""
    update.message.reply_text(msg)


def send_file(update: Update, context: CallbackContext, file):
    chat_id = update.effective_chat.id
    file_id , type_file = file
    if type_file == 'video':
        context.bot.send_video(chat_id= chat_id , video=file_id,caption=id_channel)
    elif type_file == 'video_note':
        context.bot.send_video_note(chat_id= chat_id ,video_note=file_id)
    elif type_file == 'document':
        context.bot.send_document(chat_id= chat_id , document=file_id,caption=id_channel)
    elif type_file == 'photo':
        context.bot.send_photo(chat_id= chat_id , photo=file_id,caption=id_channel)
    elif type_file == 'audio':
        context.bot.send_audio(chat_id= chat_id , audio=file_id,caption=id_channel)
    elif type_file == 'voice':
        context.bot.send_voice(chat_id= chat_id , voice=file_id,caption=id_channel)

def check_command(update: Update, context:CallbackContext):
    import pdb;pdb.set_trace()
    user_id = update.effective_user.id
    numfile = db.get_users(user_id)[0]
    try:
        num = int(update.message.text[7:])
    except:
        update.message.reply_text("سلام دوست عزیز لطفا راهنما را بخوانید ممنون")
        return False
    if num <= numfile:
        files = db.get_file(num)
        for file in files:
            try:
                send_file(update,context,file)
            except :
                pass
            sleep(3)
    else:
        update.message.reply_text(f"دوست عزیز شما تعداد {numfile} خرید کرده اید پس یک عدد کوچکتر یا مساوی وارد کنید")

def myfile(update: Update, context:CallbackContext):
    t = threading.Thread(target=check_command ,args= (update,context))
    t.start()

disp.add_handler(CommandHandler('start', start))
disp.add_handler(MessageHandler(Filters.regex("راهنما"), hellp))
disp.add_handler(MessageHandler(Filters.regex("خرید"), sell))
disp.add_handler(CommandHandler('myfile', myfile))

admin_mode = ConversationHandler(
    entry_points=[CommandHandler('adminam', adminam)],
    states={
        START_ADMIN_MODE: [MessageHandler(Filters.text, start_panel_admin)],
        ADD_USER:[MessageHandler(Filters.text , add_user)],
        SENDALL:[MessageHandler(Filters.text , send_all)],
        GET_NAME_FILE: [MessageHandler(Filters.text, get_name_file)],
        GET_FILE: [MessageHandler((Filters.document |Filters.photo | Filters.video | Filters.video_note | Filters.voice | Filters.audio), get_input_file)]
    },
    fallbacks=[CommandHandler('cancel', cancel)],)

disp.add_handler(admin_mode)

updater.start_polling()
updater.idle()
