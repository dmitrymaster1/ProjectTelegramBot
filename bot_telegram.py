
from aiogram.utils import executor
from create_bot import dp
from handlers import main_handlers
from data_base import sql_start

sql_start()

executor.start_polling(dp, skip_updates=True)