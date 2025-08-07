import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
STOCKDATA_API_KEY = os.getenv("STOCKDATA_API_KEY")
