from termcolor import colored
import os
import getpass

VER = "0.2"


def banner():
    logo = """
███████╗ █████╗  ██████╗ ██╗     ███████╗       ███████╗██╗   ██╗███████╗
██╔════╝██╔══██╗██╔════╝ ██║     ██╔════╝       ██╔════╝╚██╗ ██╔╝██╔════╝
█████╗  ███████║██║  ███╗██║     █████╗ Version █████╗   ╚████╔╝ █████╗  
██╔══╝  ██╔══██║██║   ██║██║     ██╔══╝   {0}   ██╔══╝    ╚██╔╝  ██╔══╝  
███████╗██║  ██║╚██████╔╝███████╗███████╗       ███████╗   ██║   ███████╗
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝       ╚══════╝   ╚═╝   ╚══════╝
                {1}, you have been activated                                                                   
    """
    clear()
    print(logo.format(
        VER,
        colored(getpass.getuser(), 'red', attrs=['bold'])
    )
    )


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def section(name):
    print("\n{} {}".format(
        colored("::", 'blue', attrs=['bold']),
        colored(name, attrs=['bold'])
    )
    )


def task(name):
    print('{} {}'.format(
        colored("==>", 'green', attrs=['bold']),
        colored(name, attrs=['bold'])
    )
    )


def subtask(name):
    print('{} {}'.format(
        colored("  ->", 'blue', attrs=['bold']),
        colored(name, attrs=['bold'])
    )
    )


def failure(name):
    print('{} {}'.format(
        colored("==> ERROR:", 'red', attrs=['bold']),
        colored(name, attrs=['bold'])
    )
    )


def subfailure(name):
    print('{} {}'.format(
        colored("  ->", 'red', attrs=['bold']),
        colored(name, 'red', attrs=['bold'])
    )
    )


def prompt(name):
    print('{} {}'.format(
        colored("==>", 'yellow', attrs=['bold']),
        colored(name, attrs=['bold'])),
        end=""
    )


def subprompt(name):
    print('{} {}'.format(
        colored("  ->", 'yellow', attrs=['bold']),
        colored(name, attrs=['bold'])),
        end="")
