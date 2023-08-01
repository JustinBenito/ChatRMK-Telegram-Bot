from telegram.ext import *
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, ConversationHandler


TOKEN="6617959559:AAFJBu8APBpn0byCwPW-Tz86-G8H60-SxEU"
BOT_USERNAME = "@RMKChatBot"

subjects_to_files = {
    "Maths": "maths.pdf",
    "Physics": "physics.pdf",
    "cse": "cse.pdf",
    "ece": "ece.pdf"
}

# Function to handle /tt command
def handle_timetable(update: Update, _: CallbackContext):
    update.message.reply_text("Please enter your class, section, and year (e.g., CSE B 1):")
    return "TT_INPUT"

def handle_tt_input(update: Update, _: CallbackContext):
    user_response = update.message.text
    class_data = user_response.split()
    if len(class_data) != 3:
        update.message.reply_text("Invalid format. Please enter your class, section, and year (e.g., CSE B 1):")
        return "TT_INPUT"

    department, section, year = class_data

    # Generate the filename based on the department, section, and year
    filename = f"{department}_{section}_{year}.jpeg"

    # Check if the timetable image file exists
    if os.path.exists(filename):
        # Send the timetable image to the user
        update.message.reply_photo(photo=open(filename, 'rb'))
    else:
        update.message.reply_text("Sorry, the timetable for the specified department, section, and year is not available.")

    return ConversationHandler.END

# Function to handle /dc command
def digital_content(update: Update, _: CallbackContext):
    # Create a list of buttons for each subject
    keyboard = [
        [InlineKeyboardButton("Maths", callback_data="Maths"),
         InlineKeyboardButton("Physics", callback_data="Physics")],
        [InlineKeyboardButton("cse", callback_data="cse"),
         InlineKeyboardButton("ece", callback_data="ece")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please select a subject:", reply_markup=reply_markup)

# Function to handle button presses
def button_click(update: Update, _: CallbackContext):
    query = update.callback_query
    subject = query.data

    if subject in subjects_to_files:
        file_name = subjects_to_files[subject]
        query.message.reply_document(document=open(file_name, 'rb'))
    else:
        query.message.reply_text("Sorry, the requested subject PDF is not available.")

# Function to handle /ac command
def academic_calendar(update: Update, _: CallbackContext):
    # Send the academic calendar Excel document
    academic_calendar_file = "academic.xlsx"
    update.message.reply_document(document=open(academic_calendar_file, 'rb'))

def main():
    # Initialize the Telegram Bot with your bot token
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("tt", handle_timetable))
    dp.add_handler(CommandHandler("dc", digital_content))
    dp.add_handler(CommandHandler("ac", academic_calendar))

    # Register button handler
    dp.add_handler(CallbackQueryHandler(button_click))

    # Register the handler for handling the /tt command response
    conversation_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text & ~Filters.command, handle_timetable)],
        states={
            "TT_INPUT": [MessageHandler(Filters.text & ~Filters.command, handle_tt_input)]
        },
        fallbacks=[],
    )
    dp.add_handler(conversation_handler)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
