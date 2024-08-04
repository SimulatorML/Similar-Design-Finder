import logging
from logging import LogRecord


class ColorFormatter(logging.Formatter):
    """
    A log formatter that adds color coding to log messages based on their severity level.

    This class extends the standard `logging.Formatter`, adding ANSI color codes to messages.
    Colors for different logging levels are specified in the `COLORS` dictionary.

    Attributes
    ----------
    COLORS : dict
        Maps logging levels to ANSI color codes.
    RESET : str
        ANSI code to reset the text color to default.
    """

    COLORS = {  # noqa: RUF012
        logging.DEBUG: "\033[0;36m",
        logging.INFO: "\033[1;32m",
        logging.WARNING: "\033[0;33m",
        logging.ERROR: "\033[1;31m",
        logging.CRITICAL: "\033[1;35m",
    }

    RESET = "\033[0m"

    def __init__(
        self,
        fmt: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt: str = "%Y-%m-%d %H:%M:%S",
        style: str = "%",
    ) -> None:
        """
        Initializes the formatter with the ability to add color coding to log messages.

        Parameters
        ----------
        fmt : str, optional
            The format string for initializing `logging.Formatter`.
        datefmt : str, optional
            The date format for initializing `logging.Formatter`.
        style : str, optional
            The format style, default is '%'.

        Examples
        --------
        >>> logger = logging.getLogger("my_logger")
        >>> handler = logging.StreamHandler()
        >>> handler.setFormatter(ColorFormatter())
        >>> logger.addHandler(handler)
        >>> logger.setLevel(logging.DEBUG)
        >>> logger.info("Example message")

        Creates a logger with color formatting of messages depending on the logging level.
        """

        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def format(self, record: LogRecord) -> str:
        original_msg = record.msg
        log_color = self.COLORS.get(record.levelno, self.RESET)
        record.msg = log_color + str(record.msg) + self.RESET
        formatted = super().format(record)
        record.msg = original_msg

        return log_color + formatted.replace(str(record.msg), self.RESET + str(record.msg)) + self.RESET


def setup_logging() -> None:
    """Set up logging configuration."""
    handler = logging.StreamHandler()
    formatter = ColorFormatter()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
