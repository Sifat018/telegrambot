
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import datetime

# --- CONFIGURATION ---
BOT_TOKEN = "আপনার_BotFather_থেকে_পাওয়া_Token"
OWNER_ID = 7280691598
VIP_AMOUNT = 50
VIP_DURATION_DAYS = 30
BKASH_NUMBER = "01878998648"

# In-memory store
vip_users = {}
free_counts = {}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def is_vip(user_id):
    expiry = vip_users.get(user_id)
    return expiry and datetime.datetime.now().timestamp() < expiry

def can_use_free(user_id):
    today = datetime.date.today().isoformat()
    key = f"{user_id}_{today}"
    if free_counts.get(key, 0) < 2:
        free_counts[key] = free_counts.get(key, 0) + 1
        return True
    return False

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 স্বাগতম!\n\n📊 আমি একটি চার্ট এনালাইসিস বট।\n"
        "📷 একটি চার্ট ছবি পাঠান এবং আমি তা বিশ্লেষণ করব!\n\n"
        "💎 VIP Access নিতে /buyvip কমান্ড দিন।"
    )

def getid(update: Update, context: CallbackContext):
    update.message.reply_text(f"🔑 আপনার Telegram ID: {update.effective_user.id}")

def buyvip(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"💳 VIP প্যাকেজ: {VIP_AMOUNT}৳ / {VIP_DURATION_DAYS} দিন\n"
        f"📱 Bkash নাম্বার: {BKASH_NUMBER}\n"
        "🧾 পেমেন্ট শেষে TXID পাঠান\n\n"
        "উদাহরণ:\nTXID 12345678"
    )

def analyze(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id == OWNER_ID or is_vip(user_id) or can_use_free(user_id):
        if update.message.photo:
            update.message.reply_text("🧠 আপনার চার্ট বিশ্লেষণ করা হচ্ছে...")
            update.message.reply_text(
                "📈 Chart Analysis Result:\n\n"
                "🔹 ট্রেন্ড: আপট্রেন্ড\n"
                "🔹 প্যাটার্ন: ট্রায়াঙ্গেল\n"
                "🔹 রেসিস্ট্যান্স: 2345\n"
                "🔹 সাপোর্ট: 2200"
            )
        else:
            update.message.reply_text("⚠️ দয়া করে একটি ছবি পাঠান (chart)।")
    else:
        update.message.reply_text("🔒 ফ্রি লিমিট শেষ বা আপনি VIP নন। VIP নিতে /buyvip দিন।")

def handle_txid(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    if text.startswith("TXID"):
        vip_users[user_id] = (datetime.datetime.now() + datetime.timedelta(days=VIP_DURATION_DAYS)).timestamp()
        update.message.reply_text("✅ VIP এক্সেস সফলভাবে একটিভ হয়েছে! 🎉")
    else:
        update.message.reply_text("❌ ভুল ফরম্যাট। সঠিকভাবে TXID পাঠান।")

def error_handler(update: object, context: CallbackContext):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("getid", getid))
    dp.add_handler(CommandHandler("buyvip", buyvip))
    dp.add_handler(MessageHandler(Filters.regex(r'^TXID'), handle_txid))
    dp.add_handler(MessageHandler(Filters.photo, analyze))
    dp.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
