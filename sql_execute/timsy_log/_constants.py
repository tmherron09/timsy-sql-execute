""" Timsy Log Constants """

TIMSY_LOGGER_INITIALIZED = False


def set_logger_initialized(value: bool):
    global TIMSY_LOGGER_INITIALIZED
    TIMSY_LOGGER_INITIALIZED = value

def get_logger_initialized() -> bool:
    return TIMSY_LOGGER_INITIALIZED
