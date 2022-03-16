from config import *
from place_func import *

with open('token.txt', 'r') as t:
    TOKEN = t.readline().strip()
    
if len(TOKEN) == 0:
    raise 'Please input a token'
    

updater = telegram.ext.Updater(TOKEN, use_context=True)
disp = updater.dispatcher

#PLACE HANDLERS
disp.add_handler(telegram.ext.CommandHandler("start", start))
disp.add_handler(telegram.ext.CommandHandler("help", help_))
disp.add_handler(telegram.ext.CommandHandler("contact", contact))
disp.add_handler(telegram.ext.CommandHandler("place", addplace))
disp.add_handler(telegram.ext.CommandHandler("delplace", delplace))
disp.add_handler(telegram.ext.CommandHandler("endplaces", chooseplaces))
disp.add_handler(telegram.ext.PollAnswerHandler(receive_place_poll_answer))
disp.add_handler(telegram.ext.CommandHandler("endpoll", endpoll))
disp.add_handler(telegram.ext.CommandHandler("changefinalplace", changefinalplace))

#TIME HANDLERS
disp.add_handler(telegram.ext.CommandHandler("dates", dates))

#FINAL HANDLER
disp.add_handler(telegram.ext.CommandHandler("end", end))

updater.start_polling()
updater.idle()