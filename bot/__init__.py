import logging
from configparser import ConfigParser

from bot.bot import bot
import pyromod.listen
import time

# Logging at the start to catch everything
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING,
    handlers=[
        logging.StreamHandler()
    ]
)
LOGS = logging.getLogger(__name__)


start_time = time.time()

name = 'bot'

# Read from config file
config_file = f"{name}.ini"
config = ConfigParser()
config.read(config_file)

# Extra details
__version__ = '0.0.1'
__author__ = 'pokurt'

# Global Variables
bot = bot(name)
