import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, CallbackContext, filters

# Your bot token
TOKEN = "7225691183:AAFf5xU47q9ekduGF8CyVSmP5enW_3SzheU"

# Global variables
user_data = {}  # Stores user info, deposit, and dog selection
dog_pool = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}  # Dog pools for betting
deposit_number = "+231888448949"  # Mobile money deposit number
bet_amount = 500  # Deposit amount for the game
share_link = "https://t.me/LIBDogRace_bot"  # Link to share

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Start command
async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    user_data[user.id] = {"deposit": 0, "dog_selected": None, "deposit_screenshot": None, "shared": False}

    message = (
        "**🎄 Merry Christmas and Welcome to the Dog Bet Game! 🐶🎅**\n\n"
        "🎉 Ready to join the festive fun and win big this holiday season? 🎁 Follow these steps to participate:\n\n"
        "1. **Deposit 500 LD**\n"
        f"   Send your deposit to the following number:\n   **📱 {deposit_number}**\n\n"
        "2. **Send Your Screenshot**\n"
        "   Upload a screenshot of your deposit as proof to proceed.\n\n"
        "🏆 Once your deposit is confirmed, you’re eligible to place your bet and stand a chance to win **5,000 LD or more**!\n\n"
        "---\n\n"
        "**🎁 Earn Extra Rewards! 🎉**\n"
        "Before starting your bet, share the link below with **15 people** to earn **200 coins** (valued at 200 LD):\n"
        f"🔗 [{share_link}]({share_link})\n\n"
        "---\n\n"
        "🎅 **Good luck, and may the best dog win! 🐾🎄**"
    )

    await update.message.reply_text(message, parse_mode="Markdown")

    # Ask them to send a screenshot of the deposit after the initial start message
    await update.message.reply_text("📸 Please send a screenshot of your 500 LD deposit to proceed to the next level.")

# Deposit command (screenshot verification)
async def deposit(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    if user.id not in user_data:
        user_data[user.id] = {"deposit": 0, "dog_selected": None, "deposit_screenshot": None, "shared": False}

    # Ask for screenshot
    await update.message.reply_text("📸 Please send a screenshot of your 500 LD deposit to proceed.")

# Handle deposit screenshot
async def handle_screenshot(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    if user.id not in user_data:
        user_data[user.id] = {"deposit": 0, "dog_selected": None, "deposit_screenshot": None, "shared": False}

    # Check if the message contains a photo
    if update.message.photo:
        # Check if the photo matches certain criteria, such as resolution or name, if needed
        # For now, we will just confirm that a photo is received
        photo = update.message.photo[-1].file_id  # Get the highest resolution photo
        user_data[user.id]["deposit_screenshot"] = photo

        # Provide instructions for the screenshot
        await update.message.reply_text("🎄 Thank you for sending the screenshot! Please ensure that the screenshot clearly shows your deposit of **500 LD** for verification.")

        # Confirm deposit screenshot received
        await update.message.reply_text("🎁 You can now place your bet by typing /bet.")
    else:
        # If no photo is sent
        await update.message.reply_text("🎅 Please send a valid screenshot showing your 500 LD deposit to proceed.")

# Bet command (select dog)
async def bet(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    if user.id not in user_data:
        user_data[user.id] = {"deposit": 0, "dog_selected": None, "deposit_screenshot": None, "shared": False}

    if user_data[user.id]["deposit_screenshot"] is None:
        await update.message.reply_text("🎁 You need to send a screenshot of your deposit first using /deposit.")
        return

    if not user_data[user.id]["shared"]:
        await update.message.reply_text(f"🎅 Please share the link to 15 people first: {share_link}")
        return

    keyboard = [
        [InlineKeyboardButton("Dog 1 🎄", callback_data="1"), InlineKeyboardButton("Dog 2 🎁", callback_data="2")],
        [InlineKeyboardButton("Dog 3 🐕", callback_data="3"), InlineKeyboardButton("Dog 4 🎅", callback_data="4")],
        [InlineKeyboardButton("Dog 5 🎉", callback_data="5"), InlineKeyboardButton("Dog 6 ✨", callback_data="6")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("🎉 Choose your dog to bet on this Christmas:", reply_markup=reply_markup)

# Dog selection callback handler
async def dog_selection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user = query.from_user
    dog_choice = int(query.data)

    if user.id not in user_data:
        user_data[user.id] = {"deposit": 0, "dog_selected": None, "deposit_screenshot": None, "shared": False}

    if user_data[user.id]["deposit_screenshot"] is None:
        await query.answer(text="🎅 You need to send a screenshot of your deposit first to place a bet.")
        return

    user_data[user.id]["dog_selected"] = dog_choice
    dog_pool[dog_choice].append(user.id)  # Add user to the selected dog's pool

    await query.answer(text=f"🎁 You've bet on Dog {dog_choice}! 🎉")
    await query.message.reply_text(f"🎄 Your bet has been placed on Dog {dog_choice}. Type /race to start the race!")

# Main function to set up the bot
def main() -> None:
    # Initialize the bot with your token
    application = Application.builder().token(TOKEN).build()

    # Add handlers for commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("bet", bet))
    application.add_handler(CommandHandler("deposit", deposit))

    # Add handler for callback query (dog selection)
    application.add_handler(CallbackQueryHandler(dog_selection))

    # Add handler for receiving deposit screenshots (photo messages)
    application.add_handler(MessageHandler(filters.PHOTO, handle_screenshot))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
