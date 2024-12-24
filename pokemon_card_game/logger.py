from colorama import Fore, Style, init
import datetime

# Initialize colorama
init(autoreset=True)

class Logger:
    def __init__(self, verbose=True):
        """
        Initialize the logger.
        :param verbose: If True, detailed logs will be printed. If False, only critical logs will be shown.
        """
        self.verbose = verbose

    def _get_timestamp(self):
        """
        Get the current timestamp in HH:MM:SS format.
        :return: A string representing the current timestamp.
        """
        return datetime.datetime.now().strftime("%H:%M:%S")

    def log(self, message, color=Fore.WHITE):
        """
        Print a log message if verbose mode is enabled.
        :param message: The message to log.
        :param color: The color of the message.
        """
        if self.verbose:
            print(f"{color}[{self._get_timestamp()}] {message}{Style.RESET_ALL}")

    def critical(self, message, color=Fore.RED):
        """
        Always print critical logs, regardless of verbose mode.
        :param message: The critical message to log.
        :param color: The color of the critical message.
        """
        print(f"{color}[{self._get_timestamp()}] {message}{Style.RESET_ALL}")

    def separator(self, label=None, color=Fore.CYAN):
        """
        Print a separator line with an optional label.
        :param label: A label for the separator (e.g., "Turn Start").
        :param color: The color of the separator and label.
        """
        if self.verbose:
            print(f"{color}{'=' * 40}{Style.RESET_ALL}")
            if label:
                print(f"{color}[{self._get_timestamp()}] {label}{Style.RESET_ALL}")
                print(f"{color}{'=' * 40}{Style.RESET_ALL}")
