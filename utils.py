# Some utilities
# Made by mineland
# Use it at your own accord. If anything happens do tell me


from colorama import Fore, Back, Style

def error(message):
    print(Fore.RED + str(message) + Style.RESET_ALL)
def warn(message):
    print(Fore.YELLOW + str(message) + Style.RESET_ALL)
def cPrint(color, message):
    print(color + message + Style.RESET_ALL)
def varPrint(message, variable):
    print(Fore.LIGHTWHITE_EX + message + ": " + Style.RESET_ALL + str(variable))
def success(message):
    print(Back.LIGHTGREEN_EX + Fore.BLACK + str(message) + Style.RESET_ALL)
