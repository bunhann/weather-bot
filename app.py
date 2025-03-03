import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from database import initialize_db, save_user_info, save_location
from khmer_speech import generate_khmer_audio
import requests
from dotenv import load_dotenv
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize SQLite database
initialize_db()

# Khmer messages
GENDER_QUESTION = "សូមជ្រើសរើសភេទរបស់អ្នក (ប្រុស, ស្រី, សូមមិនបញ្ជាក់):"
AGE_GROUP_QUESTION = "សូមជ្រើសរើសក្រុមអាយុរបស់អ្នក (18-25, 26-35, 36-40, 41-50, 51+):"
LOCATION_REQUEST = "សូមចែករំលែកទីតាំងបច្ចុប្បន្នរបស់អ្នក។"
WEATHER_RESPONSE = "អាកាសធាតុបច្ចុប្បន្ននៅទីតាំងរបស់អ្នកគឺ: {}°C"

# Keyboard options
GENDER_OPTIONS = [["ប្រុស", "ស្រី", "សូមមិនបញ្ជាក់"]]
AGE_GROUP_OPTIONS = [["18-25", "26-35", "36-40", "41-50", "51+"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(GENDER_QUESTION, reply_markup=ReplyKeyboardMarkup(GENDER_OPTIONS, one_time_keyboard=True))
    return "GENDER"

async def handle_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gender = update.message.text
    context.user_data['gender'] = gender
    await update.message.reply_text(AGE_GROUP_QUESTION, reply_markup=ReplyKeyboardMarkup(AGE_GROUP_OPTIONS, one_time_keyboard=True))
    return "AGE_GROUP"

async def handle_age_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    age_group = update.message.text
    context.user_data['age_group'] = age_group
    save_user_info(update.effective_user.id, context.user_data['gender'], context.user_data['age_group'])
    await update.message.reply_text(LOCATION_REQUEST)
    return "LOCATION"

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    latitude, longitude = location.latitude, location.longitude
    save_location(update.effective_user.id, latitude, longitude)

    # Fetch weather data
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = requests.get(weather_url).json()
    temperature = response['current_weather']['temperature']

    # Prepare weather response
    weather_message = WEATHER_RESPONSE.format(temperature)

    # Generate Khmer audio file
    audio_file = generate_khmer_audio(weather_message)

    # Send text message
    await update.message.reply_text(weather_message)

    # Send audio file
    with open(audio_file, 'rb') as audio:
        await update.message.reply_voice(voice=audio)

    # Clean up audio file after sending
    os.remove(audio_file)

    return "END"

def main():
     # Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        raise ValueError("Please set TELEGRAM_BOT_TOKEN environment variable")
    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            "GENDER": [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gender)],
            "AGE_GROUP": [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_age_group)],
            "LOCATION": [MessageHandler(filters.LOCATION, handle_location)],
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    main()