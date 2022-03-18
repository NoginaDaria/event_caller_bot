from config import *
from place_func import *
    
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")

if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)

if __name__ == '__main__':
    logger.info("Starting bot")
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

    #updater.start_polling()
    #updater.idle()
    run(updater)
