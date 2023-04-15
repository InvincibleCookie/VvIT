import telebot
from telebot import types
import psycopg2
import datetime

token = "token"

bot = telebot.TeleBot(token)

conn = psycopg2.connect(dbname='tabletime', user='admin', password='admin', host='localhost')
cursor = conn.cursor()

# определяем номер недели в году для текущей даты


# проверяем, является ли номер недели четным числом
if datetime.date.today().isocalendar()[1] % 2 == 0:
    week = 'чётная'
    next_week = 'нечётная'
else:
    week = 'нечётная'
    next_week = 'чётная'


def get_date_by_weekday(weekday, nxt):
    weekdays = {'ПОНЕДЕЛЬНИК': 0, 'ВТОРНИК': 1, 'СРЕДА': 2, 'ЧЕТВЕРГ': 3, 'ПЯТНИЦА': 4, 'СУББОТА': 5}
    today = datetime.date.today()
    current_weekday = today.weekday()
    days_diff = weekdays[weekday] - current_weekday
    target_date = today + datetime.timedelta(days=days_diff + nxt)
    return target_date.strftime('%d.%m')


def get_day(day, week):
    cursor.execute(
        "SELECT * FROM timetable JOIN teacher on timetable.teacher_id = teacher.id"
        " WHERE timetable.day=%s and timetable.week=%s",
        (day, week))
    answer = f'{day}  {get_date_by_weekday(day, 0)}\n'
    for row in cursor.fetchall():
        if row[5] == 18:
            answer += f'{row[4]}\n{row[8]}\n\n'
        else:
            answer += f'{row[4]}\n{row[8]}\n{row[7]}\n{row[9]} {row[3]}\n\n'
    return answer


def get_week(week, nxt):
    cursor.execute(
        "SELECT * FROM timetable JOIN teacher on timetable.teacher_id = teacher.id"
        " WHERE timetable.week=%s ORDER BY timetable.id",
        (week,))
    answer = f'ПОНЕДЕЛЬНИК {get_date_by_weekday("ПОНЕДЕЛЬНИК", nxt)}\n'
    current_day = 'ПОНЕДЕЛЬНИК'
    for row in cursor.fetchall():
        if current_day != row[2]:
            answer += f'\n{row[2]}  {get_date_by_weekday(row[2], nxt)}\n'
            current_day = row[2]
        if row[5] == 18:
            answer += f'{row[4]}\n{row[8]}\n\n'
        else:
            answer += f'{row[4]}\n{row[8]}\n{row[7]}\n{row[9]} {row[3]}\n\n'
    return answer


# [(11, 'нечётная', 'СРЕДА', 'в 314 (ОП)', '1. 09:30 - 11:05', 5, 5, 'Воронова Е. В.', 'Иностранный язык', 'Практика'), (12, 'нечётная', 'СРЕДА', 'в 301 (ОП)', '2. 11:20 - 12:55', 6, 6, 'Шаймарданова Л. К.', 'Высшая математика', 'Практика'), (13, 'нечётная', 'СРЕДА', 'в 514 (ОП)', '3. 13:10 - 14:45', 7, 7, 'Шаймарданова Л. К.', 'Высшая математика', 'Лекция'), (14, 'нечётная', 'СРЕДА', 'в 226 (ОП)', '4. 15:25 - 17:00', 8, 8, 'Вальковский С. Н.', 'Физика', 'Лекция'), (15, 'нечётная', 'СРЕДА', None, '5. 17:15 - 18:50', 18, 18, None, '<Нет пары>', None)]

# print(get_day('ПОНЕДЕЛЬНИК', week))
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Хочу", "/help", "Расписание")
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать свежую информацию о МТУСИ?', reply_markup=keyboard)


@bot.message_handler(commands=['timetable'])
def get_timetable(message):
    print(1)
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота")
    keyboard.row('На эту неделю', 'На следующую неделю')
    bot.send_message(message.chat.id, 'Выбери команду', reply_markup=keyboard)


#
@bot.message_handler(commands=['week'])
def get_week_command(message):
    bot.send_message(message.chat.id, get_week(week, 0))


@bot.message_handler(commands=['next_week'])
def get_next_week_command(message):
    bot.send_message(message.chat.id, get_week(next_week, 7))


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Я умею:\n /week - Вывести расписание на текущую неделю\n'
                                      '/next_week - Вывести расписание на следующую неделю\n'
                                      '/timetable - Выбрать день недели')


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "хочу":
        bot.send_message(message.chat.id, 'Тогда тебе сюда - https://mtuci.ru/')
    elif message.text.lower() == "расписание":
        keyboard = types.ReplyKeyboardMarkup()
        keyboard.row("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота")
        keyboard.row('На эту неделю', 'На следующую неделю')
        bot.send_message(message.chat.id, 'Выбери команду', reply_markup=keyboard)
    elif message.text.upper() in ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА']:
        bot.send_message(message.chat.id, get_day(message.text.upper(), week))
    elif message.text.lower() == 'на эту неделю':
        bot.send_message(message.chat.id, get_week(week, 0))
    elif message.text.lower() == 'на следующую неделю':
        bot.send_message(message.chat.id, get_week(next_week, 7))


bot.polling()
