# Desciption

This is a flask app developed for educational purposes for studying some common cybersecurity vulnerabilities found in client based web servers.

The webapp implements a basic stock exchange website that lets users check the stock prices in multiple exchanges throughout the world. However, the web app server is
atleast vulnerable to following attacks:

1. Dos (Denial of service attack)
1. Code Injection (SQL)
1. Leakage of Secrets
1. SSRF (Server Side request forgery)

## Steps to run the webserver app (Using Docker)

1. Clone the repo.
1. Go to [eodhd.com](https://eodhd.com/financial-apis/user-api) and get an API token.
1. Open config.py file and add the token to the `TOKEN_API` field.
1. Install Docker on your system. See: https://docs.docker.com/get-docker/
1. From command line, execute `docker build --tag python-webapp .`.
1. From command line, execute `docker run -it -p 8080:5000 --name test-project python-webapp`
1. Open browser window and go to address: `http://localhost:8080/`
1. Create an account on the website to access the webpages.

## Steps to run the webserver app (Native)

1. Clone the repo.
1. Go to [eodhd.com](https://eodhd.com/financial-apis/user-api) and get an API token.
1. Open config.py file and add the token to the `TOKEN_API` field.
1. Install python3. See https://www.python.org/downloads/
1. Run  `pip3 install -r requirements.txt` to install dependencies.
1. From command-line, run `python3 app.py --host=127.0.0.1 --port=5000`
1. Open browser window and go to address: `http://localhost:5000/`
1. Create an account on the website to access the webpages.

## Steps to start an attack

1. Install python3 on the machine running the webserver docker.
1. From a browser, create an account on the website to access the webpage.
1. cd to <repo root>\attacker directory 
1. For dos attack, run `python3 .\attacker.py -a dos -u <registered_user> -p -i 8080`
1. For code_injection attack, run `python3 .\attacker.py -a sql_injection -u <registered_user> -p -i 8080`
1. For secret_leak attack, run `python3 .\attacker.py -a secret_leak -u <registered_user> -p -i 8080  `

## Steps to enable attack mitigations in the webserver app

1. To enable a specific mitigations, open the docker container's bash prompt `docker exec -it test-project  bash`.
1. Open config.py in a command-line text editor and set a spcific mitigation flag to true. For example, to enable rate limiting to prevent dos, set `ENABLE_RATE_LIMITING_PER_USER = True`.
1. Restart the websever app in the docker for effect to take place.