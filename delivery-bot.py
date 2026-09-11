import os
import telebot

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Processed UTRs to prevent duplicate reuse
USED_UTRS = set()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "⚡ Welcome to 24TechDrop Vault!\n\n"
        "To unlock today's Digital Power Pack (₹29):\n"
        "1. Pay ₹29 via FamPay UPI: yourid@fam\n"
        "2. Enter your 12-digit UPI Reference / UTR Number below.\n\n"
        "Your bundle will unlock instantly."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_utr(message):
    utr = message.text.strip()
    
    # Check 12-digit number
    if utr.isdigit() and len(utr) == 12:
        if utr in USED_UTRS:
            bot.reply_to(message, "❌ This UTR has already been claimed.")
            return
        
        USED_UTRS.add(utr)
        bot.reply_to(message, "✅ Payment Verified! Sending your toolkit...")
        
        # Send bundle ZIP
        if os.path.exists("digital_power_pack.zip"):
            with open("digital_power_pack.zip", "rb") as f:
                bot.send_document(message.chat.id, f, caption="📦 Here is your 24TechDrop Power Pack!")
        else:
            bot.send_message(message.chat.id, "Bundle is updating. Please try in 1 minute.")
    else:
        bot.reply_to(message, "⚠️ Invalid UTR. Please enter a valid 12-digit numeric transaction ID.")

if __name__ == "__main__":
    print("Bot is listening for payments...")
    bot.infinity_polling()
