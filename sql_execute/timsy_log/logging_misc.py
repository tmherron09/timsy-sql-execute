import logging


class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO


def console_handler_factory(log_level: int = logging.INFO, log_formatter: logging.Formatter = None,
                            log_filter: logging.Filter = None, use_info_filter: bool = False) -> logging.Handler:
    log_formatter = log_formatter if log_formatter else logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - '
                                                                          '%(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(log_formatter)
    log_filter = log_filter if log_filter else (InfoFilter() if use_info_filter else None)
    if log_filter:
        ch.addFilter(log_filter)
    return ch


def file_handler_factory(log_level: int = logging.DEBUG, log_formatter: logging.Formatter = None,
                         log_filter: logging.Filter = None, file_name: str = 'timsy_app.log',
                         use_info_filter: bool = False) -> logging.Handler:
    log_formatter = log_formatter if log_formatter else logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - '
                                                                          '%(message)s')
    fh = logging.FileHandler(f'logs/{file_name}')
    fh.setLevel(log_level)
    fh.setFormatter(log_formatter)
    log_filter = log_filter if log_filter else (InfoFilter() if use_info_filter else None)
    if log_filter:
        fh.addFilter(log_filter)
    return fh


def print_logger_details(logger: logging.Logger, display_method=print()):
    """
    Print the details of a logger, including its name, level, handlers, and filters.
    :param display_method: Callback function to display the output. Default is print.
    :param logger: The logger to print details for.
    """
    # Print the logger's name, level, handlers, and filters
    display_method(f"Logger Name: {logger.name}")
    display_method(f"Logger Level: {logging.getLevelName(logger.level)}")
    display_method(f"Logger Handlers: {len(logger.handlers)}")
    display_method(f"Logger Filters: {len(logger.filters)}")

    # Iterate through each handler to print its configuration
    for i, handler in enumerate(logger.handlers, start=1):
        display_method(f"\nHandler {i}:")
        display_method(f"    Type: {type(handler).__name__}")
        display_method(f"    Level: {logging.getLevelName(handler.level)}")
        display_method(f"    Formatter: {handler.formatter}")
        display_method(f"    Filters: {len(handler.filters)}")
        for j, filter in enumerate(handler.filters, start=1):
            display_method(f"        Filter {j}: {type(filter).__name__}")


if __name__ == '__main__':
    logger = logging.getLogger('MiscLoggingTest')
    logger.setLevel(logging.DEBUG)
    console_handler = console_handler_factory()
    logger.addHandler(console_handler)
    print_logger_details(logger, logger.info)
