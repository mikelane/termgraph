from enum import Enum, unique

import colorama


@unique
class Colors(Enum):
    red = colorama.Fore.RED
    blue = colorama.Fore.BLUE
    green = colorama.Fore.GREEN
    magenta = colorama.Fore.MAGENTA
    yellow = colorama.Fore.YELLOW
    black = colorama.Fore.BLACK
    cyan = colorama.Fore.CYAN
    reset = colorama.Style.RESET_ALL
