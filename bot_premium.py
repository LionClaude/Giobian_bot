import asyncio
from telegram import Bot
import datetime
import os

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# -------------------------
# CALCOLO PASQUA
# -------------------------
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

# -------------------------
# BARRA PROGRESSO
# -------------------------
def barra_progresso(totale, rimanenti, lunghezza=20):
    completato = totale - rimanenti
    percentuale = completato / totale
    pieni = int(lunghezza * percentuale)
    vuoti = lunghezza - pieni
    return "▓" * pieni + "░" * vuoti + f" {int(percentuale*100)}%"

# -------------------------
# LOGICA INVIO
# -------------------------
async def main():
    bot = Bot(token=TOKEN)

    oggi = datetime.date.today()
    target = prossimo_giovedi_grasso()

    delta = (target - oggi).days
    if delta < 0:
        return  # protezione assoluta

    settimane = delta // 7
    giorni = delta % 7

    # totale ciclo (un anno circa)
    totale_ciclo = 365
    progresso = barra_progresso(totale_ciclo, delta)

    # -------- FREQUENZA DINAMICA --------
    invia = False

    if delta > 90:
        # periodo normale → solo giovedì
        if oggi.weekday() == 3:
            invia = True

    elif 28 < delta <= 90:
        # ultimi 3 mesi → lunedì e giovedì
        if oggi.weekday() in (0, 3):
            invia = True

    elif 0 < delta <= 28:
        # ultime 4 settimane → ogni giorno
        invia = True

    elif delta == 0:
        invia = True

    if not invia:
        return

    # -------- MESSAGGI SPECIALI --------
    if delta == 0:
        messaggio = "🎉🎭 OGGI È GIOVEDÌ GRASSO!!! 🎭🎉\nScatenatevi!"
    else:
        messaggio = (
            f"🎭 Mancano {settimane} settimane e {giorni} giorni "
            f"({delta} giorni totali)\n"
            f"📅 {target.strftime('%d/%m/%Y')}\n\n"
            f"Progresso verso il Carnevale:\n{progresso}"
        )

    await bot.send_message(chat_id=CHAT_ID, text=messaggio)

asyncio.run(main())
