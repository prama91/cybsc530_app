# Accept arguments of attack type
# Enter Login information
# Then start attack

import argparse
from ast import arg
import getpass
from pathlib import Path
import requests
import time
import aiohttp
import asyncio

attack_choices = [
    'ddos',
    'code_injection',
    'ssrf',
]

# Fill in your details here to be posted to the login form.
payload = {
    'username': 'keanu',
    'password': 'abc123'
}


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


class Hacker:
    def __init__(self, username, password):
        self.session = requests.Session()
        self.login_url = "http://127.0.0.1:5000/login"
        self.username = username
        self.password = password
        self.login()

    def login(self):
        login_data = {
            "username": self.username,
            "password": self.password
        }
        response = self.session.post(self.login_url, data=login_data)
        if response.status_code == 200:
            print(f"Logged in as {self.username}")
        else:
            print("Login failed")

    def get(self, url):
        response = self.session.get(url)
        return response.text

    def post(self, url, data):
        response = self.session.post(url, data=data)
        return response.text


parser = argparse.ArgumentParser()

parser.add_argument('-a', dest='attack', required=True, choices=attack_choices,
                    help='Supported Attacks. Use "list" to see all options.', metavar='')

parser.add_argument('-u', dest="username")
parser.add_argument('-p', dest='password',
                    action=PasswordPromptAction, type=str, required=True)

args = parser.parse_args()

print("Starting Attack ", args.attack)

hacker = Hacker(username=args.username, password=args.password)

# Record the start time
start_time = time.time()
duration = 60
while True:
    current_time = time.time()
    elapsed_time = current_time - start_time

    # Check if the desired duration has been reached
    if elapsed_time >= duration:
        print(
            f"Duration of {duration} seconds has elapsed. Exiting the loop.")
        break

    # Send an authorised request.
    r = hacker.get('http://127.0.0.1:5000/exchange/US')
