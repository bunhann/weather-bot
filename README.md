# Telegram Weather Bot (Khmer Language)

This is a Telegram bot that provides weather information in Khmer language. It uses Open-Meteo API to fetch weather data based on the user's shared location. The bot also collects user demographic information (gender and age group) and stores it in an SQLite database.

## Features
- Communicates entirely in Khmer language.
- Retrieves current weather information based on the user's location.
- Stores user information (gender, age group, location) in an SQLite database.
- Optional: Provides Khmer speech synthesis for responses.

## Prerequisites
Before running the bot, ensure you have the following installed:
- Python 3.9+
- Docker (optional, for containerized deployment)
- `mpg321` (optional, for Khmer speech playback)

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/bunhann/weather-bot.git
cd weather-bot
```
### Step 2: Clone the Repository

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```
### Step 3: Set Up the Telegram Bot
- Create a new bot using BotFather .
- Obtain the bot token.
- Replace "YOUR_TELEGRAM_BOT_TOKEN" in app.py with your bot token.

### Step 4: Run the Bot Locally
 -Run the bot locally using the following command:

 ```bash
python app.py
 ```
### Step 5: Run Using Docker (Optional)
If you prefer to run the bot in a Docker container:

Build and start the container:
```bash
docker-compose up --build
```
The bot will start running inside the container.

### Usage
1. Start a chat with the bot on Telegram.
2. Follow the prompts in Khmer language:
3. Select your gender (ប្រុស, ស្រី, មិនច្បាស់).
4. Select your age group (18-25, 26-35, 36-40, 41-50, 51+).
5. Share your current location when prompted.
6. The bot will respond with the current weather information at your location.
7. Optional: Khmer Speech Synthesis: To enable Khmer speech synthesis: Install mpg321 on your system:
```bash
sudo apt-get install mpg321
```
Ensure the khmer_speech.py module is enabled in the code.

## Contributing
Contributions are welcome! If you find any issues or want to add new features, feel free to open a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or support, contact bunhann at [bunhann.ads@gmail.com].