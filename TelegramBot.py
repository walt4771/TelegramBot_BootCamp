from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import time
import sqlite3

chat_token = 'TOKEN'
updater = Updater(token=chat_token, use_context=True)
dispacher = updater.dispatcher  # updater 에 기능 추가


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="이제 메세지를 보내셔도 됩니다\n\n"
                                                                    "/history : 최근 메세지 기록\n"
                                                                    "/dev : 개발자와 도움을 주신 분들")

def dev(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="- 개발자\n  이수민(walt4771)\n\n"
                                                                    "- PL관련 도움\n  이헌주 선배님\n  황성찬 선배님\n\n"
                                                                    "- 베타테스터\n  김나영\n  송기원\n  유경상\n  이찬우\n  최주헌\n  최다몬\n\n"
                                                                    "- Special Thanks\n  곽민규\n\n"
                                                                    "- 도와주신 모든 분들께 감사합니다")

def kungkung(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="gigyeon(기견)")

# 히스토리 쿼리
def history(update, context):
    try:
        dbConn = sqlite3.connect('Message.db')
        dbCur = dbConn.cursor()
        name = update.message.from_user.last_name + update.message.from_user.first_name

        history_query = "SELECT DATE, TIME FROM MESSAGE WHERE NAME='{}'".format(name)
        history = dbCur.execute(history_query).fetchall()
        message = ""
        messagenum = 0
        for i in history:
            j = str(i).replace(',', ' ')
            j = str(j).replace('(', '')
            j = str(j).replace(')', '')
            j = str(j).replace("'", '')
            message += "\n" + "- " + j
            messagenum += 1
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="최근에 보낸 메세지 개수는 " + str(messagenum) + "개입니다\n\n"
                                                                            "상세 정보" + message +
                                      "\n\n당신의 응원 한마디가 큰 힘이 됩니다\n감사합니다!")
        dbConn.close()
    except Exception as e:
        print(e)
        context.bot.send_message(chat_id=update.effective_chat.id, text=e)


def insert(update, context):
    name = update.message.from_user.last_name + update.message.from_user.first_name
    date = time.localtime()
    date2 = "%04d/%02d/%02d" % (date.tm_year, date.tm_mon, date.tm_mday)
    time2 = "%02d:%02d" % (date.tm_hour, date.tm_min)
    data = update.message.text

    try:
        dbConn = sqlite3.connect('Message.db')
        dbCur = dbConn.cursor()

        table_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='MESSAGE'"
        table_create = 'CREATE TABLE MESSAGE(' \
                       'ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT, MESSAGE TEXT, DATE TEXT, TIME TEXT)'
        if not dbCur.execute(table_exists).fetchone():
            dbCur.execute(table_create)

        query = "INSERT INTO MESSAGE (NAME, MESSAGE, DATE, TIME) VALUES('{}', '{}', '{}', '{}')".format(name, data, date2, time2)
        dbCur.execute(query)

        dbConn.commit()
        dbConn.close()

        print(name + "  %04d/%02d/%02d %02d:%02d" % (
            date.tm_year, date.tm_mon, date.tm_mday, date.tm_hour, date.tm_min) + '\n' + data + '\n\n')
        context.bot.send_message(chat_id=update.effective_chat.id, text="전송 대기열에 추가되었습니다. 감사합니다!")
    except Exception as e:
        print(e)
        context.bot.send_message(chat_id=update.effective_chat.id, text=e)


start_handler = CommandHandler('start', start)  # start 함수를 등록, 한글 불가
dispacher.add_handler(start_handler)

dev_handler = CommandHandler('dev', dev)
dispacher.add_handler(dev_handler)

kungkung_handler = CommandHandler('kungkung', kungkung)
dispacher.add_handler(kungkung_handler)

# 히스토리 쿼리
history_handler = CommandHandler('history', history)
dispacher.add_handler(history_handler)

insert_handler = MessageHandler(Filters.text & (~Filters.command), insert)
dispacher.add_handler(insert_handler)

updater.start_polling()  # 텔레그램 업데이트 받아오기
updater.idle()  # 메세지 입력 대기
