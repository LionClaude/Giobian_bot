from telegram import Bot
import datetime
import os

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def calcola_pasqua(anno):
    a = anno % 19
    b = anno // 100
    c = anno % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mese = (h + l - 7 * m + 114) // 31
    giorno = ((h + l - 7 * m + 114) % 31) + 1
    return datetime.date(anno, mese, giorno)

def prossimo_giovedi_grasso():
    oggi = datetime.date.today()
    anno = oggi.year
    pasqua = calcola_pasqua(anno)
    giovedi_grasso = pasqua - datetime.timedelta(days=52)

    if giovedi_grasso <= oggi:
        pasqua = calcola_pasqua(anno + 1)
        giovedi_grasso = pasqua - datetime.timedelta(days=52)

    return giovedi_grasso

oggi = datetime.date.today()
target = prossimo_giovedi_grasso()
delta = target - oggi

settimane = delta.days // 7
giorni = delta.days % 7

messaggio = (
    f"🎭 Mancano {settimane} settimane e {giorni} giorni "
    f"al prossimo Giovedì Grasso!\n"
    f"📅 Data: {target.strftime('%d/%m/%Y')}"
)

bot = Bot(token=TOKEN)
bot.send_message(chat_id=CHAT_ID, text=messaggio)
    app.run_polling()
