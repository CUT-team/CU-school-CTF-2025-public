import os
import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import dotenv

dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN")
FLAG = os.getenv("FLAG")
if not TOKEN:
    raise RuntimeError("TOKEN not configured")
if FLAG is None:
    raise RuntimeError("FLAG not configured")

REPORTS = {
    "0": FLAG,
    "1": "Жалоба на пользователя Макс Смирнов: списывал флаги у другой команды",
    "2": "Жалоба на пользователя Анна Иванова: использовала запрещенные боты для автоматизации действий",
    "3": "Жалоба на пользователя Сергей Петров: выкладывал спойлеры  в общий чат",
    "4": "Жалоба на пользователя Елена Кузнецова: размещала нецензурные материалы",
    "5": "Жалоба на пользователя Дмитрий Соколов: неоднократно нарушал правила общения",
    "6": "Жалоба на пользователя Ольга Морозова: пыталась обмануть при обмене ресурсами",
    "7": "Жалоба на пользователя Алексей Новиков: обвинял других участников без доказательств",
    "8": "Жалоба на пользователя Виктория Смирнова: отправляла флуд и спам в чат",
    "9": "Жалоба на пользователя Никита Федоров: предлагал приватные ссылки на пиратский контент",
    "10": "Жалоба на пользователя Мария Попова: публиковала личные данные других участников",
    "11": "Жалоба на пользователя Игорь Васильев: без разрешения изменял настройки канала",
}

JOKES = [
    "Штирлиц играл в карты и проигрался. Но Штирлиц умел делать хорошую мину при плохой игре. Когда Штирлиц покинул компанию, мина сработала.",
    "Идет Штирлиц ночью по городу, навстречу мужик бородатый и в чалме — Ах, будь он не Ладен, подумал Штирлиц.",
    "Штирлиц и Мюллер ездили по очереди на танке. Очередь редела, но не расходилась...",
    "Штирлиц стрелял вслепую. Слепая испугалась и побежала скачками, но качки быстро отстали.",
    "Штирлиц шёл по улице, когда внезапно перед ним что-то упало. Штирлиц поднял глаза — это были глаза профессора Плейшнера.",
    "Штирлиц вышел из дома и увидел как четыре бугая ставили трактор на попа. — Бедный пастор Шлаг, — подумал Штирлиц.",
    "Штирлиц вытащил из сейфа записку Мюллера. Мюллеру было очень больно и он сильно ругался.",
    "Штирлиц упал с балкона и чудом зацепился за другой балкон. Чудо потом распухло и мешало ходить...",
    "Штирлицу попала в голову пуля. 'Разрывная,' — раскинул мозгами Штирлиц.",
    "Штирлиц стоял на своем. Это была любимая пытка Мюллера.",
    "Штирлиц настаивал на своем. Настойка получалась крепкой, но слегка мутноватой.",
    "Штирлиц всю ночь топил камин. На утро камин утонул.",
    "Штирлиц стоял над картой мира. Его неудержимо рвало на родину.",
    "Штирлиц сел в свой автомобиль и сказал шоферу: 'Трогай!' Шофер потрогал, Штирлиц поехал.",
    "Штирлиц и Кэт вышли на связь. Но в центре об этом узнали только через девять месяцев.",
    "Штирлиц долго смотрел в одну точку. Потом в другую. 'Двоеточие!' — наконец-то смекнул Штирлиц.",
    "Письмо из центра до Штирлица не дошло... Пришлось читать во второй раз.",
    "Штирлиц выстрелил вслепую. Слепая упала как подкошенная. Подкошенную Штирлиц застрелил накануне.",
    "Лампа горела, но света не давала. 'Что-то тут не так...' — подумал Штирлиц и погасил лампу. Света дала.",
    "Штирлиц шел по лесу и напоролся на сук. Суки разбежались.",
    "Штирлиц сунул вилку в розетку, когда ему тактично намекнули, что из розетки едят ложечкой.",
    "Во время секретного совещания в бункер Гитлера с шашкой наголо ворвался Штирлиц и закричал: — Порублю, гады. Гады скинулись по рублю. Штирлиц собрал деньги и ушел.",
    "Штирлиц сидел у камина и вязал. Вязание успокаивало Штирлица. После окончания вязания у камина остался лежать связанный Мюллер.",
    "Штирлиц поднял трубку и услышал томный голос радистки Кэт: — Вам, наверное, не спится без менcя? — Почему же? Спиться я могу и без вас, — ответил Штирлиц и налил очередной стакан водки.",
    "Штирлиц шёл в Дрезден с трудом разбирая дорогу. Наутро железная дорога от Берлина до Дрездена была полностью разобрана...",
    "Штирлицу за шиворот упала гусеница. 'Где-то взорвался танк,' — подумал Штирлиц.",
    "Штирлиц ехал на машине по берегу моря. 'Выйду посмотрю отлив на море,' — подумал Штирлиц... и отлив, посмотрел.",
    "Штирлиц приготовился к бою, а пришла гёрл...",
    "Штирлиц вышел из моря и лёг на гальку. Галька обиделась и ушла.",
]

COMMANDS = {
    "report": "Выдать отчет по ID",
    "admins": "Показать список организаторов чата",
    "dice": "Бросить кубик (1-6)",
    "joke": "Рассказать шутку",
    "flip": "Подбросить монету",
    "roll": "Бросить число от 1 до N (по умолчанию 100)",
    "help": "Показать список команд",
}

async def delete_ctf_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg and msg.text and "ctf{" in msg.text:
        try:
            await msg.delete()
        except Exception:
            pass

async def is_organizer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    member = await update.effective_chat.get_member(update.effective_user.id)
    if member.status == "creator":
        return True
    return member.status == "administrator" and member.custom_title == "организатор"

async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_organizer(update, context):
        await update.message.reply_text("Вы не организатор")
        return
    if not context.args:
        await update.message.reply_text("Пожалуйста, укажите ID отчета: /report <id>")
        return
    report = REPORTS.get(context.args[0])
    await update.message.reply_text(report or "Отчет с таким ID не найден.")

async def admins_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admins = await update.effective_chat.get_administrators()
    names = [a.user.full_name for a in admins if a.status == "creator" or a.custom_title == "организатор"]
    text = "Организаторы чата:\n" + "\n".join(names) if names else "В этом чате нет организаторов."
    await update.message.reply_text(text)

async def dice_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🎲 Вы бросили: {random.randint(1, 6)}")

async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(JOKES))

async def flip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = random.choice(["Орёл", "Решка"])
    await update.message.reply_text(f"🪙 Выпало: {choice}")

async def roll_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    max_val = int(context.args[0]) if context.args and context.args[0].isdigit() else 100
    await update.message.reply_text(f"🎲 Вы бросили: {random.randint(1, max_val)} (от 1 до {max_val})")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lines = [f"/{cmd} - {desc}" for cmd, desc in COMMANDS.items()]
    await update.message.reply_text("Доступные команды:\n" + "\n".join(lines))

def main():
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_ctf_messages))
    app.add_handler(CommandHandler("report", report_command))
    app.add_handler(CommandHandler("admins", admins_command))
    app.add_handler(CommandHandler("dice", dice_command))
    app.add_handler(CommandHandler("joke", joke_command))
    app.add_handler(CommandHandler("flip", flip_command))
    app.add_handler(CommandHandler("roll", roll_command))
    app.add_handler(CommandHandler("help", help_command))
    app.run_polling()

if __name__ == "__main__":
    main()
