from colorama import init, Fore
init()


def error(msg):
    print(Fore.RED + msg + Fore.RESET)


def warning(msg):
    print(Fore.YELLOW + msg + Fore.RESET)


def ok(msg):
    print(Fore.GREEN + msg + Fore.RESET)


def info(msg):
    print(Fore.BLUE + msg + Fore.RESET)
