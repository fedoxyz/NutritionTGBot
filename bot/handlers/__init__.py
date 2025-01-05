from logger import logger


from .start_handler import setup_start_handler
from .menu_handler import setup_menu_handlers
from .nutr_balance_handler import setup_nutr_balance_handlers
from .index_hei_handler import setup_hei_handlers
from .chem_ratio_handler import setup_chem_ratio_handlers
from .data_source_handler import setup_data_source_handlers
from .json_receipt_handler import setup_json_receipt_handlers
from .receipt_overview_handler import setup_receipt_process_handlers
from .product_overview_handler import setup_product_overview_handlers
from .photo_receipt_handler import setup_photo_receipt_handlers

all_handlers = [
    setup_start_handler,
    setup_menu_handlers,
    setup_nutr_balance_handlers,
    setup_hei_handlers,
    setup_chem_ratio_handlers,
    setup_data_source_handlers,
    setup_json_receipt_handlers,
    setup_receipt_process_handlers,
    setup_product_overview_handlers,
    setup_photo_receipt_handlers
]

def setup_all_handlers(app):
    for handler_setup in all_handlers:
        handler_setup(app)

