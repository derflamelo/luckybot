from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import random
import datetime

# -------------------- CONFIG --------------------
TOKEN = "8276795508:AAHwNyVviE7cJydWoaBfaO3bQXo_7HT4fx0"  # Ton token Telegram
ADMIN_ID = 7530082416  # Ton ID Telegram
pending_verifications = {}  # Stock temporaire des IDs en attente
# ------------------------------------------------

# --- Commande /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("🛫 S’inscrire", url="https://lkvn.cc/c712705d")],
        [InlineKeyboardButton("🔂 Déjà inscrit", callback_data="already")],
        [InlineKeyboardButton("❤️ Vérifier mon ID", callback_data="verify")]
    ]
    text = (
        "🤖 NOUVEAU BOT AVIATOR – SIGNALS PRÉCIS À 94% DE RÉUSSITE !\n\n"
        "Tu veux gagner gros sur LUCKY JET ? Ce bot révolutionnaire te donne des signaux ultra fiables avec ✅ 94% de réussite !\n"
        "⚠️ Le bot fonctionne uniquement avec les comptes inscrits avec le code promo : VVIP250 sur 1win !\n\n"
        "📩 Mon inbox : @yoanive\n"
        "Mon canal : https://t.me/derflamelo25"
    )
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

# --- Boutons Inline ---
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data in ["already", "verify"]:
        await query.message.reply_text("🆔 Veuillez saisir votre ID 1WIN pour la vérification :")

# --- Réception d'un ID utilisateur ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if text.isdigit() and len(text) in [8, 9]:
        pending_verifications[user_id] = text
        await update.message.reply_text("⏳ Vérification en cours…")

        # Notification à l'admin
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🔔 Nouvelle demande de vérification : {update.effective_user.first_name}\n🆔 ID : {text}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Valider", callback_data=f"approve_{user_id}"),
                 InlineKeyboardButton("❌ Refuser", callback_data=f"reject_{user_id}")]
            ])
        )
    else:
        await update.message.reply_text("❌ Veuillez saisir un identifiant 1WIN valide (8 ou 9 chiffres).")

# --- Validation Admin ---
async def admin_verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("approve_"):
        user_id = int(data.split("_")[1])
        await context.bot.send_message(
            chat_id=user_id,
            text="✅ Votre ID a été validé !\nVous pouvez maintenant recevoir vos prédictions Lucky Jet 🎯",
            reply_markup=ReplyKeyboardMarkup([["📊 Prochaine cote", "🆘 Aide"]], resize_keyboard=True)
        )
        await query.message.reply_text("✅ Validation effectuée.")
    elif data.startswith("reject_"):
        user_id = int(data.split("_")[1])
        await context.bot.send_message(chat_id=user_id, text="❌ Votre vérification a été refusée.")
        await query.message.reply_text("❌ Rejeté.")

# --- Prédiction Lucky Jet ---
async def show_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text("⏳ PRÉDICTION EN COURS...")

    coeff1 = round(random.uniform(2.5, 4.5), 2)
    coeff2 = round(coeff1 + random.uniform(0.3, 1.5), 2)
    hour = datetime.datetime.now().strftime("%H:%M")
    next_hour = (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%H:%M")
    trust = random.randint(80, 95)

    prediction = (
        f"🛫 PRÉDICTIONS ~ AVIATOR 🛫\n\n"
        f"📊 Coefficients : {coeff1}x - {coeff2}x\n"
        f"⏰ Horaire : {hour} - {next_hour}\n"
        f"📈 Fiabilité : {trust}%\n\n"
        f"💰 Conseil : Misez intelligemment selon votre budget."
    )

    await context.bot.send_message(
        chat_id=chat_id,
        text=prediction,
        reply_markup=ReplyKeyboardMarkup([["📊 Prochaine cote", "🏠 Menu principal"]], resize_keyboard=True)
    )

# --- Aide utilisateur ---
async def help_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📩 Besoin d’aide ? Contacte : @yoanive")

# --- Lancement du bot ---
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(CallbackQueryHandler(admin_verify, pattern=r"^(approve_|reject_)\d+$"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(MessageHandler(filters.Regex("📊 Prochaine cote"), show_prediction))
app.add_handler(MessageHandler(filters.Regex("🆘 Aide"), help_user))

print("✅ Bot lancé avec succès !")
app.run_polling()
