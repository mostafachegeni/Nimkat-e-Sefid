#TODO:
# 1. DOS Attack         -> Done!
# 2. Gamification       -> Done! *** can be continued... ***
# 3. Timer for Exam     -> Done!
# 4. GIF "how to use"
# 5. Showing Results    -> Done!
# 6. ...

# Every day Tasks:
#                   +++++1. clear    candidate black list
#                   +++++2. clear    member black list
#                   +++++3. Reset    passed_exams to 'xxxxxx' for all Subscribers in database
#                   +++++4. Upload   new exams arabi_matn_001_question.png, ...
#                   +++++4. Upload   new sols  arabi_matn_001_solution.png, ...
#                   #***#5. Reset    arabi_matn_solution, ...
#                   +++++6. Reset    total_number_of_questions_arabi_matn, ...
#                   #***#7. Reload   flask_app.py

import sys
from flask import Flask, request
import telepot
import urllib3
import time


from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
#from pprint import pprint
#from telepot import message_identifier
from telepot.delegate import pave_event_space, per_chat_id, create_open

from config import Config
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate

#import telebot
#from telebot import types

#proxy_url = "http://proxy.server:3128"
#telepot.api._pools = {
#    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
#}
#telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))


class MessageCounter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._count = 0

    def on_chat_message(self, msg):
        self._count += 1
        self.sender.sendMessage(self._count)

secret = "nb117195-g9e2-4b05-bu2b-d11n5117wb72"

#bot = telepot.Bot('649688438:AAGqdFTnqYhYmLKA5KiX0fzQI6oUiZBrYYw')
#bot = telepot.DelegatorBot('649688438:AAGqdFTnqYhYmLKA5KiX0fzQI6oUiZBrYYw', [
#    pave_event_space()(
#        per_chat_id(), create_open, MessageCounter, timeout=10),
#])



#bot = telepot.DelegatorBot('761896715:AAFb5at-4i4YBntwwFLo0JIYXy62nqq8ZpE', [
#    pave_event_space()(
#        per_chat_id(), create_open, MessageCounter, timeout=10),
#])

bot = telepot.DelegatorBot('764893890:AAHzMzbLQ5VvTGeZzbZqdpRoJQ2JbF6rB_4', [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=10),
])



bot.setWebhook("https://www.nimkatesefid.ir/{}".format(secret), max_connections=1)

application = Flask(__name__)
application.config.from_object(Config)
db = SQLAlchemy(application)
#migrate = Migrate(application, db)

#print("OK_1")

DOS_01 = 30 #Not message nor callback_query
DOS_02 = 30 #Not chat
DOS_03 = 30 #(Not text nor contact) or (File not from admin)
DOS_04 = 30 #Not /start nor arabi nor zaban nor adabiat
DOS_05 = 30 #A contact that chat_id != user_id
DOS_06 = 30 #A callback_query that its chat_id is not in Examinees

DOS_11 = 10 # /start
DOS_12 = 10 # contact
DOS_13 = 10 # arabi or zaban or adabiat
DOS_14 = 1  # callback_query                #Deactivated

DOS_Threshold = 150

chat_id_admin_1 = 122377423
#chat_id_admin_2 = 591324836
#chat_id_admin_3 = 92247028
chat_id_admin_3 = 1111111

arabi_matn          = "درک مطلب عربی"
arabi_mani          = "تست ترجمه عربی"
zaban_matn          = "درک مطلب زبان"
zaban_mani          = "تست ترجمه زبان"
zaban_cloze         = "کلوز زبان"
adabiat_gherabat    = "تست قرابت معنایی ادبیات"


arabi_matn_solution         = '114431233'
zaban_matn_solution         = '3224'
arabi_mani_solution         = '32143244'
zaban_mani_solution         = '213141212433'
zaban_cloze_solution        = '21324'
adabiat_gherabat_solution   = '143214322'

total_number_of_questions_arabi_matn        = len(arabi_matn_solution)
total_number_of_questions_zaban_matn        = len(zaban_matn_solution)
total_number_of_questions_arabi_mani        = len(arabi_mani_solution)
total_number_of_questions_zaban_mani        = len(zaban_mani_solution)
total_number_of_questions_zaban_cloze       = len(zaban_cloze_solution)
total_number_of_questions_adabiat_gherabat  = len(adabiat_gherabat_solution)


def remained_exam(i):
    switcher={
            0:arabi_matn,
            1:zaban_matn,
            2:arabi_mani,
            3:zaban_mani,
            4:zaban_cloze,
            5:adabiat_gherabat,
         }
    return switcher.get(i,"---")


class Subscriber(db.Model):
    id              = db.Column(db.Integer,    primary_key=True)
    username        = db.Column(db.String(15), index=True, unique=True)    # Phone Number
    chat_id         = db.Column(db.String(10), index=True)                 # Chat id
    first_name      = db.Column(db.String(20), index=True)
    passed_exams    = db.Column(db.String(10), index=True)
    golden_points   = db.Column(db.Integer,    index=True)
    bronze_points   = db.Column(db.Integer,    index=True)
    #email = db.Column(db.String(120), index=True, unique=True)
    #password_hash = db.Column(db.String(128))
    def __repr__(self):
        return '<User: Username={} , Exam Number={}>'.format(self.username, self.passed_exams)

class Examinee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username                    = db.Column(db.String(10), index=True, unique=True) # Chat id
    question_number             = db.Column(db.Integer,    index=True)
    total_number_of_questions   = db.Column(db.Integer,    index=True)
    type_of_exam                = db.Column(db.String(20), index=True)
    message_id                  = db.Column(db.Integer,    index=True)              # Message id
    answers                     = db.Column(db.String(20), index=True)              # Answers
    start_time                  = db.Column(db.Integer,    index=True)
    def __repr__(self):
        return '<User: Username = {} , Question Number = {}>'.format(self.username, self.question_number)

class Candidate_Black_List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(64), index=True, unique=True) # Chat id
    DOS_Counter = db.Column(db.Integer,    index=True)
    def __repr__(self):
        return '<User: Username = {} , DOS_01 = {}>'.format(self.username, self.DOS_Counter)

class Member_Black_List(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(64), index=True, unique=True) # Chat id
    def __repr__(self):
        return '<User: Username = {} >'.format(self.username)

class File_of_Exam_List(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    File_Name   = db.Column(db.String(64), index=True, unique=True)
    File_id     = db.Column(db.String(64), index=True)
    def __repr__(self):
        return '<User: File_Name = {} , File_id = {}>'.format(self.File_Name, self.File_id)

def update_Candidate_and_Member_Black_Lists(chat_id, DOS_Count):
    candidate = Candidate_Black_List.query.filter_by(username = str(chat_id)).first()
    if candidate is None:
        candidate = Candidate_Black_List(username    = str(chat_id),
                                         DOS_Counter = DOS_Count  )
        db.session.add(candidate)
        db.session.commit()
    else:
        candidate.DOS_Counter += DOS_Count
        db.session.commit()

    if candidate.DOS_Counter > DOS_Threshold:
        member = Member_Black_List.query.filter_by(username = str(chat_id)).first()
        if member is None:
            if (chat_id != chat_id_admin_1) and (chat_id != chat_id_admin_3):
                member = Member_Black_List(username = candidate.username)
                db.session.add(member)
                db.session.commit()
                db.session.delete(candidate)
                db.session.commit()

    return

def clear_all_database():
    #bot.sendMessage(chat_id, "Before")
    subs = Subscriber.query.all()
    for s in subs:
        #bot.sendMessage(chat_id, "Subscriber username = {}".format(s.username) )
        db.session.delete(s)
        db.session.commit()
    subs = Examinee.query.all()
    for s in subs:
        #bot.sendMessage(chat_id, "Examinee username = {}".format(s.username) )
        db.session.delete(s)
        db.session.commit()

    #bot.sendMessage(chat_id, "After")
    subs = Candidate_Black_List.query.all()
    for s in subs:
        #bot.sendMessage(chat_id, "Subscriber username = {}".format(s.username) )
        db.session.delete(s)
        db.session.commit()
    subs = Member_Black_List.query.all()
    for s in subs:
        #bot.sendMessage(chat_id, "Examinee username = {}".format(s.username) )
        db.session.delete(s)
        db.session.commit()

    subs = File_of_Exam_List.query.all()
    for s in subs:
        #bot.sendMessage(chat_id, "Examinee username = {}".format(s.username) )
        db.session.delete(s)
        db.session.commit()
    return


def start_exam(chat_id, exam_type, number_of_questions):
    missing = Examinee.query.filter_by(username = str(chat_id)).first()
    if missing is None:
        new_examinee = Examinee(username = str(chat_id),
                                question_number = 1,
                                answers = ' ',
                                total_number_of_questions = number_of_questions,
                                type_of_exam = exam_type)

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [
                            InlineKeyboardButton(text = "پرسش {}:".format(new_examinee.question_number), callback_data='p_1_1')
                        ],
                        [
                            InlineKeyboardButton(text = "1",    callback_data='p_2_1'),
                            InlineKeyboardButton(text = "2",    callback_data='p_2_2'),
                            InlineKeyboardButton(text = "3",    callback_data='p_2_3'),
                            InlineKeyboardButton(text = "4",    callback_data='p_2_4')
                        ],
                        [
                            InlineKeyboardButton(text = "پرسش بعدی",    callback_data='p_3_1')
                        ]
                   ])

        if exam_type == arabi_matn:
            #photo = open('/home/pythonnimkatsefid/mysite/arabi_matn_001_question.png', 'rb')
            #photo_id = arabi_matn_001_question_file["document"]["file_id"]
            file_name = "%arabi_matn_question%"
        elif exam_type == zaban_matn:
            #photo = open('/home/pythonnimkatsefid/mysite/zaban_matn_001_question.png', 'rb')
            #photo_id = zaban_matn_001_question_file["document"]["file_id"]
            file_name = "%zaban_matn_question%"
        elif exam_type == arabi_mani:
            #photo = open('/home/pythonnimkatsefid/mysite/arabi_mani_001_question.png', 'rb')
            #photo_id = arabi_mani_001_question_file["document"]["file_id"]
            file_name = "%arabi_mani_question%"
        elif exam_type == zaban_mani:
            #photo = open('/home/pythonnimkatsefid/mysite/zaban_mani_001_question.png', 'rb')
            #photo_id = zaban_mani_001_question_file["document"]["file_id"]
            file_name = "%zaban_mani_question%"
        elif exam_type == zaban_cloze:
            #photo = open('/home/pythonnimkatsefid/mysite/zaban_cloze_001_question.png', 'rb')
            #photo_id = zaban_cloze_001_question_file["document"]["file_id"]
            file_name = "%zaban_cloze_question%"
        elif exam_type == adabiat_gherabat:
            #photo = open('/home/pythonnimkatsefid/mysite/adabiat_gherabat_001_question.png', 'rb')
            #photo_id = adabiat_gherabat_001_question_file["document"]["file_id"]
            file_name = "%adabiat_gherabat_question%"
        else:
            return

        #m_file = File_of_Exam_List.query.filter_by(File_Name = file_name).first()
        #m_file = db.session.query(File_of_Exam_List).filter(File_of_Exam_List.File_Name.like(file_name)).first()
        m_file = File_of_Exam_List.query.filter(File_of_Exam_List.File_Name.like(file_name)).first()

        if m_file is not None:
            photo_id = m_file.File_id
        else:
            bot.sendMessage(chat_id, "آزمونک مورد نظر شما در سامانه موجود نیست. شما می‌توانید در آزمونک دیگری شرکت کنید.")
            return

        bot.sendMessage(chat_id, "گزینه مورد نظر خود برای هر پرسش را به‌ترتیب انتخاب کنید. اگر پاسخ پرسشی را نمی‌دانید، روی دکمه «پرسش بعدی» کلیک کنید:")
        bot.sendChatAction(chat_id, action = 'upload_photo')
        #test = bot.sendDocument(chat_id, "BQADBAADRQUAAj8hYFBJuW1-0OqyyAI", reply_markup = keyboard)
        test = bot.sendDocument(chat_id, photo_id, reply_markup = keyboard)
        #test = bot.sendPhoto(chat_id, photo, reply_markup = keyboard)
        #bot.sendMessage(chat_id, test)
        new_examinee.message_id = test['message_id']
        new_examinee.start_time = int(time.time())
        db.session.add(new_examinee)
        db.session.commit()

    else:
        bot.sendMessage(chat_id, "شما هنوز آزمونک قبلی خود را به اتمام نرسانده اید. اگر به آزمونک قبلی خود دسترسی ندارید، می توانید ربات را حذف کنید و دوباره ثبت نام نمایید" )
        #msg_identifier = telepot.message_identifier(msg)
        #bot.editMessageText(, "Updated Message!", )
        #bot.deleteMessage(msg_identifier)
    return

number_of_starts = 0;

@application.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    #return "hello !!!"
    update = request.get_json()
    #print("OK_2")
    if "message" in update:
        msg = update["message"]
        #pprint(update)
        if "chat" in msg:
            content_type, chat_type, chat_id = telepot.glance(msg, flavor='chat')

            if chat_id is None:
                return "BAD"

            #bot.sendMessage(chat_id, "msg={}".format(msg) )

            #if chat_id == chat_id_admin_1:
            #    member = Member_Black_List.query.filter_by(username = str(chat_id)).first()
            #    if member is not None:
            #        db.session.delete(member)
            #        db.session.commit()

            member = Member_Black_List.query.filter_by(username = str(chat_id)).first()
            if member is not None:
                #bot.sendMessage(chat_id, "Black LIST")
                #db.session.delete(member)
                #db.session.commit()
                #bot.sendMessage(chat_id, "After")
                bot.sendMessage(chat_id, "شما در لیست سیاه ربات قرار گرفته‌اید. لطفا ۲۴ ساعت بعد دوباره مراجعه کنید.")
                return "BAD"

            if content_type == "text":
                m_text = msg["text"]
                if m_text == "/start":
                    #clear_all_database()
                    #bot.sendMessage(chat_id, "DOS Attack 11 !")
                    update_Candidate_and_Member_Black_Lists(chat_id, DOS_11)

                    keyboard_2 = ReplyKeyboardMarkup(keyboard=[
                                    [
                                        KeyboardButton(text = "«عضویت با شماره موبایل»", request_contact = True),
                                    ],
                                    #[
                                    #    KeyboardButton(text = "گزینه اضافی", request_contact = False)
                                    #]
                               ])
                    bot.sendMessage(chat_id, "برای دریافت سرویس بهتر، شماره موبایل خود را ثبت نمایید", reply_markup = keyboard_2)
                    global number_of_starts
                    number_of_starts = number_of_starts + 1

                elif m_text == arabi_matn:
                    #bot.sendMessage(chat_id, "DOS Attack 13 !")
                    update_Candidate_and_Member_Black_Lists(chat_id, DOS_13)
                    start_exam(chat_id, arabi_matn, total_number_of_questions_arabi_matn)
                elif m_text == zaban_matn:
                    #bot.sendMessage(chat_id, "DOS Attack 13 !")
                    update_Candidate_and_Member_Black_Lists(chat_id, DOS_13)
                    start_exam(chat_id, zaban_matn, total_number_of_questions_zaban_matn)
                elif m_text == arabi_mani:
                    #bot.sendMessage(chat_id, "DOS Attack 13 !")
                    update_Candidate_and_Member_Black_Lists(chat_id, DOS_13)
                    start_exam(chat_id, arabi_mani, total_number_of_questions_arabi_mani)
                elif m_text == zaban_mani:
                    #bot.sendMessage(chat_id, "DOS Attack 13 !")
                    update_Candidate_and_Member_Black_Lists(chat_id, DOS_13)
                    start_exam(chat_id, zaban_mani, total_number_of_questions_zaban_mani)
                elif m_text == zaban_cloze:
                    #bot.sendMessage(chat_id, "DOS Attack 13 !")
                    update_Candidate_and_Member_Black_Lists(chat_id, DOS_13)
                    start_exam(chat_id, zaban_cloze, total_number_of_questions_zaban_cloze)
                elif m_text == adabiat_gherabat:
                    #bot.sendMessage(chat_id, "DOS Attack 13 !")
                    update_Candidate_and_Member_Black_Lists(chat_id, DOS_13)
                    start_exam(chat_id, adabiat_gherabat, total_number_of_questions_adabiat_gherabat)

                elif (chat_id == chat_id_admin_1) or (chat_id == chat_id_admin_3):
                    if m_text == "show black lists":
                        Cans = Candidate_Black_List.query.all()
                        bot.sendMessage(chat_id, "#######################")
                        bot.sendMessage(chat_id, "Black List Candidates:")
                        for c in Cans:
                            bot.sendMessage(chat_id, "id={} Username={} DOS_Counter={}".format(c.id, c.username, c.DOS_Counter) )
                        bot.sendMessage(chat_id, "------------------------------------------------------------------------")
                        Mems = Member_Black_List.query.all()
                        bot.sendMessage(chat_id, "Black List Members:")
                        for m in Mems:
                            bot.sendMessage(chat_id, "id={} Username={} ".format(m.id, m.username) )
                        bot.sendMessage(chat_id, "#######################")

                    elif m_text == "show subscriber":
                        Subs = Subscriber.query.all()
                        bot.sendMessage(chat_id, "Subscribers:")
                        for s in Subs:
                            bot.sendMessage(chat_id, "id={} phone_number={} chat_id={} first_name={} passed_exams={} golden_points={} bronze_points={}".format(s.id, s.username, s.chat_id, s.first_name, s.passed_exams, s.golden_points, s.bronze_points) )
                            #username, chat_id, passed_exams, first_name, golden_points, bronze_points

                    elif m_text == "show examinee":
                        examinee = Examinee.query.all()
                        bot.sendMessage(chat_id, "Examinees:")
                        for e in examinee:
                            bot.sendMessage(chat_id, "id={} username={} type_of_exam={}".format(e.id, e.username, e.type_of_exam) )
                            #username, question_number, total_number_of_questions, type_of_exam, message_id, answers

                    elif m_text == "show exam files":
                        exams = File_of_Exam_List.query.all()
                        bot.sendMessage(chat_id, "Exam Files:")
                        for e in exams:
                            bot.sendMessage(chat_id, "id={} File_Name={} File_id={}".format(e.id, e.File_Name, e.File_id) )
                            #username, question_number, total_number_of_questions, type_of_exam, message_id, answers

                    elif m_text == "clear subscriber":
                        subs = Subscriber.query.all()
                        for s in subs:
                            #bot.sendMessage(chat_id, "Subscriber username = {}".format(s.username) )
                            db.session.delete(s)
                            db.session.commit()

                    elif m_text == "clear examinee":
                        examinee = Examinee.query.all()
                        for e in examinee:
                            #bot.sendMessage(chat_id, "Examinee username = {}".format(s.username) )
                            db.session.delete(e)
                            db.session.commit()

                    elif m_text == "clear candidate black list":
                        #bot.sendMessage(chat_id, "After")
                        cans = Candidate_Black_List.query.all()
                        for c in cans:
                            #bot.sendMessage(chat_id, "Subscriber username = {}".format(s.username) )
                            db.session.delete(c)
                            db.session.commit()

                    elif m_text == "clear member black list":
                        mems = Member_Black_List.query.all()
                        for m in mems:
                            #bot.sendMessage(chat_id, "Examinee username = {}".format(s.username) )
                            db.session.delete(m)
                            db.session.commit()

                    elif m_text == "clear exam files":
                        exams = File_of_Exam_List.query.all()
                        for e in exams:
                            #bot.sendMessage(chat_id, "Exam name = {}".format(e.File_Name) )
                            db.session.delete(e)
                            db.session.commit()

                    elif m_text == "reset passed exams for all":
                        subs = Subscriber.query.all()
                        for s in subs:
                            s.passed_exams = "xxxxxx"
                            db.session.commit()
                            #bot.sendMessage(chat_id, "Subscriber username = {}".format(s.username) )
                            #db.session.delete(s)
                            #db.session.commit()

                    elif m_text == "number of starts":
                        bot.sendMessage(chat_id, "number of starts = {}".format(number_of_starts) )


                else:
                    #bot.sendMessage(chat_id, "DOS Attack 04 !")
                    update_Candidate_and_Member_Black_Lists(chat_id, DOS_04)

            elif "document" in msg:
                if (chat_id == chat_id_admin_1) or (chat_id == chat_id_admin_3):
                    if "arabi_matn_question" in msg["document"]["file_name"]:
                        file_name = "%arabi_matn_question%"
                    elif "zaban_matn_question" in msg["document"]["file_name"]:
                        file_name = "%zaban_matn_question%"
                    elif "arabi_mani_question" in msg["document"]["file_name"]:
                        file_name = "%arabi_mani_question%"
                    elif "zaban_mani_question" in msg["document"]["file_name"]:
                        file_name = "%zaban_mani_question%"
                    elif "zaban_cloze_question" in msg["document"]["file_name"]:
                        file_name = "%zaban_cloze_question%"
                    elif "adabiat_gherabat_question" in msg["document"]["file_name"]:
                        file_name = "%adabiat_gherabat_question%"
                    elif "arabi_matn_solution" in msg["document"]["file_name"]:
                        file_name = "%arabi_matn_solution%"
                    elif "zaban_matn_solution" in msg["document"]["file_name"]:
                        file_name = "%zaban_matn_solution%"
                    elif "arabi_mani_solution" in msg["document"]["file_name"]:
                        file_name = "%arabi_mani_solution%"
                    elif "zaban_mani_solution" in msg["document"]["file_name"]:
                        file_name = "%zaban_mani_solution%"
                    elif "zaban_cloze_solution" in msg["document"]["file_name"]:
                        file_name = "%zaban_cloze_solution%"
                    elif "adabiat_gherabat_solution" in msg["document"]["file_name"]:
                        file_name = "%adabiat_gherabat_solution%"
                    else:
                        bot.sendMessage(chat_id, "File's Name was not Correct = {}".format(msg["document"]["file_name"]) )
                        return "BAD"

                    #m_file = File_of_Exam_List.query.filter_by(File_Name = file_name).first()
                    m_file = File_of_Exam_List.query.filter(File_of_Exam_List.File_Name.like(file_name)).first()

                    if m_file is None:
                        #bot.sendMessage(chat_id, "NO")
                        new_file = File_of_Exam_List(File_Name = msg["document"]["file_name"], File_id = msg["document"]["file_id"])
                        db.session.add(new_file)
                        db.session.commit()
                    else:
                        #bot.sendMessage(chat_id, "YES")
                        m_file.File_Name = msg["document"]["file_name"]
                        db.session.commit()
                        m_file.File_id = msg["document"]["file_id"]
                        db.session.commit()

                else:
                    #bot.sendMessage(chat_id, "DOS Attack 03 !")
                    update_Candidate_and_Member_Black_Lists(chat_id, DOS_03)


            elif "contact" in msg:
                if msg["contact"]["user_id"] == chat_id:
                    #bot.sendMessage(chat_id, "DOS Attack 12 !")
                    update_Candidate_and_Member_Black_Lists(chat_id, DOS_12)

                    #bot.sendMessage(chat_id, msg )
                    user_phone_number = msg["contact"]["phone_number"]
                    if user_phone_number[0] == '+':
                        user_phone_number = user_phone_number[1:len(user_phone_number)]

                    missing = Subscriber.query.filter_by(username = user_phone_number).first()
                    if missing is None:
                        #bot.sendMessage(chat_id, "None" )
                        new_subscriber = Subscriber(username = user_phone_number )
                        new_subscriber.chat_id = str(chat_id)
                        if len(msg["contact"]["first_name"]) > 20:
                            new_subscriber.first_name = msg["contact"]["first_name"][0:20]
                        else:
                            new_subscriber.first_name = msg["contact"]["first_name"]
                        new_subscriber.passed_exams = 'xxxxxx'
                        new_subscriber.golden_points = 0
                        new_subscriber.bronze_points = 0
                        db.session.add(new_subscriber)
                        db.session.commit()
                    else:
                        bot.sendMessage(missing.chat_id, "شماره موبایل شما قبلاً در سامانه ثبت شده است" )
                        #bot.sendMessage(missing.chat_id, "We have your phone number: Phone Number = {} , Chat id = {} ".format(missing.username, missing.chat_id) )

                    m_examinee = Examinee.query.filter_by(username = str(chat_id)).first()
                    if m_examinee is not None:
                        db.session.delete(m_examinee)
                        db.session.commit()

                    remove_keyboard = ReplyKeyboardRemove()
                    keyboard = ReplyKeyboardMarkup(keyboard=[
                                    [
                                        KeyboardButton(text = arabi_matn),
                                        KeyboardButton(text = arabi_mani)
                                    ],
                                    [
                                        KeyboardButton(text = zaban_matn),
                                        KeyboardButton(text = zaban_mani)
                                    ],
                                    [
                                        KeyboardButton(text = zaban_cloze)
                                    ],
                                    [
                                        KeyboardButton(text = adabiat_gherabat)
                                    ]
                               ])
                    bot.sendMessage(chat_id, "آزمونک مورد نظر خود را انتخاب نمایید" , reply_markup = keyboard)
                    #ReplyKeyboardRemove(remove_keyboard = True)
                else:
                    #bot.sendMessage(chat_id, "DOS Attack 05 !")
                    update_Candidate_and_Member_Black_Lists(chat_id, DOS_05)
                    bot.sendMessage(chat_id, "لطفاً از گزینه «عضویت با شماره موبایل» استفاده نمایید.")

            else:
                #bot.sendMessage(chat_id, "DOS Attack 03 !")
                update_Candidate_and_Member_Black_Lists(chat_id, DOS_03)
        else:
            if "from" in msg:
                if "id" in msg["from"]:
                    #bot.sendMessage(msg["from"]["id"], "DOS Attack 02 !")
                    update_Candidate_and_Member_Black_Lists(msg["from"]["id"], DOS_02)

    elif "callback_query" in update:
        msg = update["callback_query"]
        #bot.sendMessage(chat_id, update)
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        #bot.sendMessage(from_id, "Got it !")
        #bot.sendMessage(from_id, "query_id: {}".format(query_id))
        #bot.sendMessage(from_id, "from_id: {}".format(from_id))
        #bot.sendMessage(from_id, "query_data: {}".format(query_data))

        if from_id is None:
            return "BAD"

        # Much Overhead to Detect DOS Attack: ******
        #member = Member_Black_List.query.filter_by(username = str(from_id)).first()
        #if member is not None:
        #    bot.sendMessage(from_id, "شما در لیست سیاه ربات قرار گرفته‌اید. لطفا ۲۴ ساعت بعد دوباره مراجعه کنید.")
        #    return "BAD"
        #bot.sendMessage(from_id, "DOS Attack 14 !")
        #update_Candidate_and_Member_Black_Lists(from_id, DOS_14)

        m_examinee = Examinee.query.filter_by(username = str(from_id)).first()

        if query_data == 'p_1_1':
            return "OK"

        if m_examinee is not None:
            if query_data == 'p_3_1':
                m_examinee.answers = m_examinee.answers + 'x'
                db.session.commit()
                bot.answerCallbackQuery(query_id, text='شما به پرسش {} پاسخ ندادید.'.format( len(m_examinee.answers)-1 ))
            elif query_data == 'p_2_1':
                m_examinee.answers = m_examinee.answers + '1'
                db.session.commit()
                bot.answerCallbackQuery(query_id, text='پاسخ شما به پرسش {}: گزینه 1'.format( len(m_examinee.answers)-1 ))
            elif query_data == 'p_2_2':
                m_examinee.answers = m_examinee.answers + '2'
                db.session.commit()
                bot.answerCallbackQuery(query_id, text='پاسخ شما به پرسش {}: گزینه 2'.format( len(m_examinee.answers)-1 ))
            elif query_data == 'p_2_3':
                m_examinee.answers = m_examinee.answers + '3'
                db.session.commit()
                bot.answerCallbackQuery(query_id, text='پاسخ شما به پرسش {}: گزینه 3'.format( len(m_examinee.answers)-1 ))
            elif query_data == 'p_2_4':
                m_examinee.answers = m_examinee.answers + '4'
                db.session.commit()
                bot.answerCallbackQuery(query_id, text='پاسخ شما به پرسش {}: گزینه 4'.format( len(m_examinee.answers)-1 ))

            if m_examinee.question_number < m_examinee.total_number_of_questions:
                m_examinee.question_number += 1
                db.session.commit()
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                [
                                    InlineKeyboardButton(text = "پرسش {}:".format(m_examinee.question_number), callback_data='p_1_1')
                                ],
                                [
                                    InlineKeyboardButton(text = "1",    callback_data='p_2_1'),
                                    InlineKeyboardButton(text = "2",    callback_data='p_2_2'),
                                    InlineKeyboardButton(text = "3",    callback_data='p_2_3'),
                                    InlineKeyboardButton(text = "4",    callback_data='p_2_4')
                                ],
                                [
                                    InlineKeyboardButton(text = "پرسش بعدی",    callback_data='p_3_1')
                                ]
                   ])
                bot.editMessageCaption((m_examinee.username, m_examinee.message_id), reply_markup = keyboard)
                #bot.editMessageText((chat_id, message_id), "Modify!", reply_markup = keyboard)
                #bot.editMessageReplyMarkup((chat_id, message_id), reply_markup = keyboard)
                #bot.editMessageCaption((chat_id, message_id), reply_markup = keyboard)
                #bot.deleteMessage((chat_id, message_id))
                #bot.answerCallbackQuery(query_id, text='Got it !!!')
            else:
                exam_elapsed_time = int(time.time()) - m_examinee.start_time
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                       [
                            InlineKeyboardButton(text = "پایان!", callback_data = 'p_1_1')
                        ]
                   ])

                bot.editMessageCaption((m_examinee.username, m_examinee.message_id), reply_markup = keyboard)

                m_subscriber = Subscriber.query.filter_by(chat_id = m_examinee.username).first()
                if m_subscriber is None:
                    bot.sendMessage(m_examinee.username, "شماره موبایل شما هنوز در سامانه ثبت نشده است. برای دریافت پاسخ‌نامه می‌توانید با استفاده از دکمه‌ی «عضویت با شماره موبایل» در سامانه ثبت‌نام کنید.")
                    db.session.delete(m_examinee)
                    db.session.commit()
                    return

                solution = ' '
                if m_examinee.type_of_exam == arabi_matn:
                    i = 0
                    solution += arabi_matn_solution
                    #photo = open('/home/pythonnimkatsefid/mysite/arabi_matn_001_solution.png', 'rb')
                    #photo_id = arabi_matn_001_solution_file["document"]["file_id"]
                    file_name = "%arabi_matn_solution%"
                elif m_examinee.type_of_exam == zaban_matn:
                    i = 1
                    solution += zaban_matn_solution
                    #photo = open('/home/pythonnimkatsefid/mysite/zaban_matn_001_solution.png', 'rb')
                    #photo_id = zaban_matn_001_solution_file["document"]["file_id"]
                    file_name = "%zaban_matn_solution%"
                elif m_examinee.type_of_exam == arabi_mani:
                    i = 2
                    solution += arabi_mani_solution
                    #photo = open('/home/pythonnimkatsefid/mysite/arabi_mani_001_solution.png', 'rb')
                    #photo_id = arabi_mani_001_solution_file["document"]["file_id"]
                    file_name = "%arabi_mani_solution%"
                elif m_examinee.type_of_exam == zaban_mani:
                    i = 3
                    solution += zaban_mani_solution
                    #photo = open('/home/pythonnimkatsefid/mysite/zaban_mani_001_solution.png', 'rb')
                    #photo_id = zaban_mani_001_solution_file["document"]["file_id"]
                    file_name = "%zaban_mani_solution%"
                elif m_examinee.type_of_exam == zaban_cloze:
                    i = 4
                    solution += zaban_cloze_solution
                    #photo = open('/home/pythonnimkatsefid/mysite/zaban_cloze_001_solution.png', 'rb')
                    #photo_id = zaban_cloze_001_solution_file["document"]["file_id"]
                    file_name = "%zaban_cloze_solution%"
                elif m_examinee.type_of_exam == adabiat_gherabat:
                    i = 5
                    solution += adabiat_gherabat_solution
                    #photo = open('/home/pythonnimkatsefid/mysite/adabiat_gherabat_001_solution.png', 'rb')
                    #photo_id = adabiat_gherabat_001_solution_file["document"]["file_id"]
                    file_name = "%adabiat_gherabat_solution%"
                else:
                    return

                temp = list(m_subscriber.passed_exams)
                if temp[i] == '{}'.format(i):
                    flag = False # This was not a new exam
                else:
                    flag = True  # This was a new exam
                    temp[i] = '{}'.format(i)
                #bot.sendMessage(m_examinee.username, "flag = {}".format(flag) )

                m_subscriber.passed_exams = "".join(temp)
                db.session.commit()

                number_of_correct_answers = 0
                your_answers = "کارنامه آزمونک:\n\n"
                for j in range(1, len(m_examinee.answers)):
                    your_answers += 'پرسش {}:   [{}]      (پاسخ صحیح: {})\n'.format(j, m_examinee.answers[j], solution[j])
                    if m_examinee.answers[j] == solution[j]:
                        number_of_correct_answers += 1
                your_answers += "\nشما از مجموع {} پرسش به {} مورد پاسخ صحیح دادید.".format(m_examinee.total_number_of_questions, number_of_correct_answers)
                your_answers += "\nزمان صرف شده: {} دقیقه و {} ثانیه".format(int(exam_elapsed_time/60), exam_elapsed_time%60)

                bot.sendMessage(m_examinee.username, your_answers)
                #bot.sendMessage(m_examinee.username, "پاسخ های شما:{}".format(m_examinee.answers) )
                #bot.sendMessage(m_examinee.username, "سلام {}\n شما از میان شش آزمونک امروز در {} آزمونک شرکت کرده‌اید.".format(m_subscriber.first_name, 5))

                flag_increment_bronze_points = False
                if flag:
                    if number_of_correct_answers >= (len(m_examinee.answers) - 1)/2:
                        flag_increment_bronze_points = True
                        m_subscriber.bronze_points += 1
                        db.session.commit()
                    if m_subscriber.bronze_points >= 6:
                        m_subscriber.bronze_points = 0
                        db.session.commit()
                        m_subscriber.golden_points += 1
                        db.session.commit()
                    hint = '\n\nبا شرکت در هر آزمونک جدید در یک روز و کسب درصد بالای ۵۰٪، یک امتیاز برنزی دریافت می‌کنید.'
                    hint += '\nبه‌ازای هر شش امتیاز برنزی نیز یک امتیاز طلایی خواهید داشت.'
                    if m_subscriber.passed_exams != '012345':
                        remining_exams_for_today = "آزمونک‌های باقی‌مانده برای امروز:\n"
                        for k in range(len(m_subscriber.passed_exams)):
                            if m_subscriber.passed_exams[k] != '{}'.format(k):
                                remining_exams_for_today += "- {}\n".format(remained_exam(k))
                        remining_exams_for_today += "\nموفق باشید"
                    else:
                        remining_exams_for_today = "آفرین!\nشما در تمام آزمونک‌های امروز شرکت کردید.\n"
                        remining_exams_for_today += "\nموفق باشید"

                else:
                    hint = "لطفا برای جلوگیری از افزایش ترافیک سرور، از شرکت چندباره در یک آزمونک در یک روز پرهیز بفرمایید.\nبا توجه به اینکه آزمونک‌ها هر ۲۴ ساعت یکبار به‌روزرسانی می‌شوند با چند بار شرکت کردن در یک آزمونک، امتیاز شما افزایش پیدا نخواهد کرد."
                    if m_subscriber.passed_exams != '012345':
                        remining_exams_for_today = "آزمونک‌های باقی‌مانده برای امروز:\n"
                        for k in range(len(m_subscriber.passed_exams)):
                            if m_subscriber.passed_exams[k] != '{}'.format(k):
                                remining_exams_for_today += "- {}\n".format(remained_exam(k))
                        remining_exams_for_today += "\nموفق باشید"
                    else:
                        remining_exams_for_today = "آزمونک‌های باقی‌مانده برای امروز:\n"
                        remining_exams_for_today += "شما در تمام آزمونک‌های امروز شرکت کرده‌اید."

                points_string = 'امتیازات شما:\n'
                points_string += '- امتیاز طلایی: {}\n'.format(m_subscriber.golden_points)
                points_string += '- امتیاز برنزی: {}\n'.format(m_subscriber.bronze_points)
                if flag_increment_bronze_points == False:
                    points_string += "(به علت کسب درصد کمتر از ۵۰٪ در این آزمونک، امتیاز برنزی شما افزایش نیافته است.)"

                bot.sendMessage(m_examinee.username, hint + "\n\n" + points_string + "\n\n" + remining_exams_for_today)

                #m_file = File_of_Exam_List.query.filter_by(File_Name = file_name).first()
                #m_file = db.session.query(File_of_Exam_List).filter(File_of_Exam_List.File_Name.like(file_name)).first()
                m_file = File_of_Exam_List.query.filter(File_of_Exam_List.File_Name.like(file_name)).first()

                if m_file is not None:
                    photo_id = m_file.File_id
                else:
                    bot.sendMessage(m_examinee.username, "متأسفانه پاسخ‌نامه این آزمونک در سامانه وجود ندارد. بابت اشکال پیش آمده پوزش می‌طلبیم.")
                    db.session.delete(m_examinee)
                    db.session.commit()
                    return

                bot.sendChatAction(m_examinee.username, action = 'upload_photo')
                #test = bot.sendDocument(m_examinee.username, photo, caption = "پاسخ نامه تشریحی")
                test = bot.sendDocument(m_examinee.username, photo_id, caption = "پاسخ نامه تشریحی")
                #test = bot.sendPhoto(m_examinee.username, photo, caption = "پاسخ نامه تشریحی")

                db.session.delete(m_examinee)
                db.session.commit()

        else:
            #bot.sendMessage(from_id, "DOS Attack 06 !")
            update_Candidate_and_Member_Black_Lists(from_id, DOS_06)


    #else:
        # DO Nothing! ****
        #bot.sendMessage(chat_id???, "DOS Attack 01 !")
        #update_Candidate_and_Member_Black_Lists(chat_id???, DOS_01)

    #bot.sendMessage(chat_id???, update)

    return "OK"



#from socket import gethostname

#if __name__ == '__main__':
#    db.create_all()
#    print("OK_3")
#    if 'liveconsole' not in gethostname():
#        app.run()

#print("OK_4")


#@app.route('/{}'.format(secret), methods=["POST"])
#def telegram_webhook():
#    update = request.get_json()
#    if "message" in update:
#        text = update["message"]["text"]
#        chat_id = update["message"]["chat"]["id"]
#        bot.sendMessage(chat_id, "web-> '{}'".format(text))
#    return "OK"
