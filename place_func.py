from config import *
from plot_date_pic import *

# PLACE FUNC
def start(update, context):
    update.message.reply_text(text="""
    Всем привет\! Я бот Event Caller, пришел помочь организовать вашу встречу\.
    \nЭтот бот задумывается как органайзер идей по времени и месту встречи\. Я призван превратить неструктурированное шумное обсуждение в продуктивное общение и сэкономить всем время ☺️\.
    \nДля начала выберем, где встречаемся\. Предгалайте места по шаблону \n/place _место_
    \nКогда идеи закончатся, дайте мне команду \n /endplaces
    \nЧтобы удалить место, напишите \n/delplace _место_
    """, parse_mode='MarkdownV2')
    
def addplace(update, context):
    global places
    if context.args:
        new_place = ' '.join(context.args[0:])
        places.add(new_place)
    else:
        update.message.reply_text("Укажите место после тэга")
    
def delplace(update, context):
    global places
    if context.args:
        del_place = ' '.join(context.args[0:])
        places.remove(del_place)
    else:
        update.message.reply_text("Укажите место после тэга")
    
def chooseplaces(update, context):
    global places
    if len(places) == 0:
        update.message.reply_text("Выберите хотя бы одно место!")
        return
    elif len(places) == 1:
        global final_place
        final_place = places.pop()
        update.message.reply_text("Отлично, место единогласно выбрано!")
        print_time_instructions(update, context)
        return
    
    update.message.reply_text("""
    Отлично, с местами определились. Теперь проведем голосование. \nКогда будете готовы подвести итоги - вызовите /endpoll""")
    
    global poll_places
    poll_places = dict.fromkeys(places, 0)
    places = list(places)
    
    question = "Какое место кажется оптимальным?"
    message = context.bot.send_poll(
        chat_id=update.effective_chat.id, 
        question=question, 
        options=places, 
        is_anonymous=False, 
        allows_multiple_answers=True,
    )
    payload = {
        message.poll.id: {
            "options": places,
            "message_id": message.message_id,
            "chat_id": update.effective_chat.id,
            "answers": 0,
        }
    }
    context.bot_data.update(payload)
    
    
def receive_place_poll_answer(update, context):
    answer = update.poll_answer
    poll_id = answer.poll_id
    options = context.bot_data[poll_id]["options"]
    
    selected_options = answer.option_ids
    
    for selected_option_id in selected_options:
        selected_option = options[selected_option_id]
        poll_places[selected_option] += 1
    context.bot_data[poll_id]["answers"] += 1
    
    
def endpoll(update, context):
    if not poll_places:
        update.message.reply_text("Что-то пошло не так")
    else:
        if sum(poll_places.values()) == 0:
            update.message.reply_text("Должен проголосовать хотя бы один человек")
            return
        priority_places = [k for k, v in sorted(poll_places.items(), key=lambda item: item[1])][::-1]
        medals_string = ''
        for i in range(len(priority_places)):
            if i == 0:
                medals_string += f'🥇 {priority_places[i]} ->'
            elif i == 1 and poll_places[priority_places[i]] > 0:
                medals_string += f'🥈 {priority_places[i]} ->'
            elif i == 2 and poll_places[priority_places[i]] > 0:
                medals_string += f'🥉 {priority_places[i]} ->'
            else:
                break
        update.message.reply_text(medals_string[:-2])
        
        if len(priority_places) >= 2 and poll_places[priority_places[0]] == poll_places[priority_places[1]]:
            update.message.reply_text(f"Видимо, большинство хочет пойти сюда: {priority_places[0]} или сюда: {priority_places[1]}. Я выбрал первый вариант. Если вы хотите изменить место, дайте мне команду /changefinalplace")
        else:
            update.message.reply_text(f"Видимо, большинство хочет пойти сюда: {priority_places[0]}. Если вы хотите изменить место, дайте мне команду /changefinalplace")
        global final_place
        final_place = priority_places[0]
        print_time_instructions(update, context)
        
    
def changefinalplace(update, context):
    if context.args:
        global final_place
        final_place = ' '.join(context.args[0:])
        
    else:
        update.message.reply_text("Укажите место после тэга")
        
        
#TIME FUNC
from datetime import date

def print_time_instructions(update, context):
    update.message.reply_text("А пока перейдем к выбору подходящего всем времени\! \nПеречислите удобные даты через запятую без пробелов \n/dates _ДД\.ММ\.ГГ,ДД\.ММ\.ГГ,ДД\.ММ\.ГГ_\. \nМожно вставлять интервалы _ДД\.ММ\.ГГ\-ДД\.ММ\.ГГ_\.\n\nКогда будете готовы окончательно определиться с датой \- пишите мне с тэгом /end _дата_, и я оформлю итоги\!", parse_mode='MarkdownV2')
    
def date_to_datetimeobj(date):
    return datetime.datetime.strptime(date, '%d.%m.%y')
    
def parse_dates(dates):
    dates = dates.split(',')
    res = []
    for date in dates:
        if '-' not in date:
            res.append(date_to_datetimeobj(date))
        else:
            start_date, end_date = date.split('-')
            start_date, end_date = [date_to_datetimeobj(i) for i in [start_date, end_date]]
            delta = end_date - start_date
            for i in range(delta.days + 1):
                res.append(start_date + datetime.timedelta(days=i))
    return res

def dates(update, context):
    if context.args and len(context.args) == 1:
        dates = context.args[0]
        dates = parse_dates(dates)
        global all_dates
        for date in dates:
            all_dates.append(date)
        update.message.reply_text("Спасибо! Изобразил обновленное удобное время:")
        plot_name = plot_date_pic(all_dates)
        file = open(plot_name, 'rb') 
        context.bot.sendPhoto(chat_id=update.message.chat.id, photo=file)
        file.close()
        os.remove(plot_name)
    else:
        update.message.reply_text("Укажите даты после тэга в указанном формате")
        
        
def end(update, context):
    if context.args:
        final_time = ' '.join(context.args[0:])
    else:
        update.message.reply_text("Укажите выбранную дату после тэга")
    global final_place
    final_time = '\.'.join(final_time.split('.'))
    update.message.reply_text(f"Ура\! Место и время встречи определено 😉\nМесто\: *{final_place}*\nДата\: *{final_time}*", parse_mode='MarkdownV2')

    
def help_(update, context):
    update.message.reply_text("""
    Можно вызвать вот эти команды:\n
    /start -> поздороваемся еще раз!\n
    /contact -> получить контакт создателя \n
    /help -> получить справку по командам \n
    """)
    
    
def contact(update, context):
    update.message.reply_text("Привет! Написала этого бота @d_diotima")