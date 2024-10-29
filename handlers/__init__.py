from typing import Awaitable, Callable, Dict
from telegram import Update
from telegram.ext import ContextTypes

from logs.logger import logger

from .start_handler import setup_start_handler
from .menu_handler import setup_menu_handlers
from .nutr_balance_handler import setup_nutr_balance_handlers
from .index_hei_handler import setup_hei_handlers
from .chem_ratio_handler import setup_chem_ratio_handlers
from .data_source_handler import setup_data_source_handlers
from .check_process_handler import setup_check_process_handlers

all_handlers = [
    setup_start_handler,
    setup_menu_handlers,
    setup_nutr_balance_handlers,
    setup_hei_handlers,
    setup_chem_ratio_handlers,
    setup_data_source_handlers,
    setup_check_process_handlers
]

def setup_all_handlers(app):
    for handler_setup in all_handlers:
        handler_setup(app)

