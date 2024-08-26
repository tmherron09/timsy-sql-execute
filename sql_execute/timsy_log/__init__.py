import os

# check if directory "logs" exists
if not os.path.isdir("logs"):
    os.makedirs("logs", exist_ok=True)

from ._constants import get_logger_initialized

from .logging_misc import (
    InfoFilter,
    console_handler_factory,
    print_logger_details,
)

from .timsy_logger import (
    init_root_logger,
    getLogger
)

init_root_logger()
