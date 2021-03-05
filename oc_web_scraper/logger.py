from datetime import datetime

from pathlib import Path

import logging

from oc_web_scraper import errors as _CUSTOM_ERRORS


class Logger:
    def __init__(
        self, enable_logging: bool, log_to_file: bool, log_path: str, log_level: str
    ):
        self.enable_logging = enable_logging

        if not self.enable_logging:
            return

        self.logger = None
        self.log_to_file = log_to_file
        self.log_path = log_path
        self.log_level = None
        self.set_log_level(log_level=log_level)

        self.logger = logging.getLogger("main")
        self.logger.setLevel(self.log_level)

        if log_to_file:
            self.start_logging_to_file()
        else:
            self.start_logging_to_terminal()

    def set_log_level(self, log_level: str):
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
        """Main logging function, initiates and configures the logger object."""

        time = datetime.now().strftime("%Y-%m-%d-%H%M%S")

        absolute_path = Path(self.log_path).joinpath(
            "web_scraper_{time}.log".format(time=time)
        )

        file_handler = logging.FileHandler(absolute_path)
        file_handler.setLevel(self.log_level)

        self.logger.addHandler(file_handler)

    def start_logging_to_terminal(self):

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self.log_level)

        self.logger.addHandler(stream_handler)

    def write(self, log_type: str, text: str):
        """Uses logger object to write to file."""

        if not self.enable_logging:
            return

        if log_type == "debug":
            self.logger.debug(text)
        elif log_type == "info":
            self.logger.info(text)
        elif log_type == "warning":
            self.logger.warning(text)
        elif log_type == "error":
            self.logger.error(text)
        elif log_type == "critical":
            self.logger.critical(text)
