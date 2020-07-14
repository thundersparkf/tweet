import scraper
from scraper import Twint
import database
from database import DataBase

class Extractor:
    def __init__(self):
        self.twint = Twint()
        self.db = DataBase()
    def pull_user_blob(self):
        self.db.load_data()