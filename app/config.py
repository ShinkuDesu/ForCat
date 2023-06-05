from dotenv import load_dotenv
import os


load_dotenv()

DB_URL = os.environ.get('DB_URL')
ALGORITHM = os.environ.get('ALGORITHM')
SECRET_KEY = os.environ.get('SECRET_KEY')
THREAD_MESSAGE_STANDART_LIMIT = 50