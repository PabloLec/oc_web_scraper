from datetime import datetime

from pathlib import Path

import logging

from oc_web_scraper import errors as _CUSTOM_ERRORS


class Logger:
    """Logger class manages logging process depending on config.yml file params.
    If enabled, will log to a file or to terminal with 'logging' library.

    Attributes:
        logger (logging.Logger): Proper 'logging' logger object if enabled.
        log_to_file (bool): If True, will not output anything in terminal
        and redirect stdout to selected file.
        log_path (str): Local path for log file.
        log_level (str): Log level desired by user. Should match a level
        of 'library' log level.
    """

    def __init__(
        self, enable_logging: bool, log_to_file: bool, log_path: str, log_level: str
    ):
        """Constructor for Logger class.

        Args:
            enable_logging (bool): If True, will enable logging throughout script.
            log_to_file (bool): If True, will not output anything in terminal
            log_path (str): Local path for log file.
            log_level (str): Log level desired by user. Should match a level
            of 'library' log level.
        """

        self.enable_logging = enable_logging

        if not self.enable_logging:
            return

        self.logger = None
        self.log_to_file = log_to_file
        self.log_path = log_path
        self.log_level = None
        self.set_log_level(log_level=log_level)
        self.log_format = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S"
        )

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.log_level)

        if log_to_file:
            self.start_logging_to_file()
        else:
            self.start_logging_to_terminal()

    def set_log_level(self, log_level: str):
        """Takes string given in config.yml file and set log level
        to corresponding 'logging' library level.

        Args:
            log_level (str): Log level given in config.yml.
        Raises:
            _CUSTOM_ERRORS.CouldNotParseLogLevel: If log level given in
            config.yml does not match any 'logging' library level.
        """

        log_level = log_level.lower()

        if log_level == "debug":
            self.log_level = logging.DEBUG
        elif log_level == "info":
            self.log_level = logging.INFO
        elif log_level == "warning":
            self.log_level = logging.WARNING
        elif log_level == "error":
            self.log_level = logging.ERROR
        elif log_level == "critical":
            self.log_level = logging.CRITICAL
        else:
            raise _CUSTOM_ERRORS.CouldNotParseLogLevel(level=log_level)

    def start_logging_to_file(self):
        """If set so in config.yml, initiates logging to a file."""

        time = datetime.now().strftime("%Y-%m-%d-%H%M%S")

        absolute_path = Path(self.log_path).joinpath(
            "web_scraper_{time}.log".format(time=time)
        )

        file_handler = logging.FileHandler(absolute_path)
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(self.log_format)

        self.logger.addHandler(file_handler)

    def start_logging_to_terminal(self):
        """If set so in config.yml, initiates logging to terminal."""

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self.log_level)
        stream_handler.setFormatter(self.log_format)

        self.logger.addHandler(stream_handler)

    def write(self, log_level: str, message: str):
        """Writes given message to either a file or terminal.
        Handles returning if logging is disabled.
        Logger object of 'logging' library handles not writing
        anything if message level is lower than global set log level.

        Args:
            log_level (str): Message log level.
            message (str): Message text to print.
        """

        if not self.enable_logging:
            return

        # Inform user when saving process starts if logging only outputs to file
        if "Starting saving process" in "message" and self.log_to_file:
            print("Saving...")

        if log_level == "debug":
            self.logger.debug(message)
        elif log_level == "info":
            self.logger.info(message)
        elif log_level == "warning":
            self.logger.warning(message)
        elif log_level == "error":
            self.logger.error(message)
        elif log_level == "critical":
            self.logger.critical(message)
