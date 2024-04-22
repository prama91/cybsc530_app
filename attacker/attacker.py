# Accept arguments of attack type
# Enter Login information
# Then start attack

import argparse
from ast import arg
import getpass
from pathlib import Path

attack_choices = [
    'ddos',
    'code_injection',
    'ssrf',
]


class PasswordPromptAction(argparse.Action):
    def __init__(self,
                 option_strings,
                 dest=None,
                 nargs=0,
                 default=None,
                 required=False,
                 type=None,
                 metavar=None,
                 help=None):
        super(PasswordPromptAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            default=default,
            required=required,
            metavar=metavar,
            type=type,
            help=help)

    def __call__(self, parser, args, values, option_string=None):
        password = getpass.getpass()
        setattr(args, self.dest, password)


parser = argparse.ArgumentParser()

parser.add_argument('-a', dest='attack', required=True, choices=attack_choices,
                    help='Supported Attacks. Use "list" to see all options.', metavar='')

parser.add_argument('-u', dest="username")
parser.add_argument('-p', dest='password',
                    action=PasswordPromptAction, type=str, required=True)

args = parser.parse_args()

print("Hello ", args.username)
print("Starting Attack ", args.attack)
