import re
import sys
import argparse
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from api.financial_data import EODHDAPIsDataFetcher
from config import API_TOKEN


parser = argparse.ArgumentParser(description="EODHD APIs")
parser.add_argument(
    "--host",
    type=str,
    help="Web service IP (default: 127.0.0.1)",
)
parser.add_argument(
    "--port",
    type=int,
    help="Web service port (default: 5000)",
)
parser.add_argument("--debug", action="store_true", help="Enable debugging")
args = parser.parse_args()


# Listen on local host
http_host = "0.0.0.0"
if args.host is not None:
    p = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    if p.match(args.host):
        http_host = args.host
    else:
        parser.print_help(sys.stderr)

# Listen on local port
http_port = 5000
if args.port is not None:
    if args.port >= 0 and args.port <= 65535:
        http_port = args.port
    else:
        parser.print_help(sys.stderr)


app = Flask(__name__)
login_manager = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'this is a secret key '
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    # is_active = db.Column(db.Boolean(), default=True)

    def __repr__(self):
        return f'<User {self.username}>'


data_fetcher = EODHDAPIsDataFetcher(API_TOKEN)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('Home.html')


@app.route("/welcome")
def welcome():
    exchanges = data_fetcher.fetch_exchanges()
    return render_template("exchanges.html", exchanges=exchanges)


@app.route("/exchange/<code>")
def exchange_markets(code):
    markets = data_fetcher.fetch_exchange_markets(code)
    return render_template("markets.html", code=code, markets=markets)


@app.route("/exchange/<code>/<market>/<granularity>")
def exchange_market_data(code, market, granularity):
    candles = data_fetcher.fetch_exchange_market_data(
        code, market, granularity)
    return render_template("data.html", code=code, market=market, granularity=granularity, candles=candles)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('welcome'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = password

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('registeration.html')


@app.route('/logout_page')
def logout_page():
    logout_user()
    return render_template('logout.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('logout_page'))


if __name__ == "__main__":
    app.run(host=http_host, port=http_port, debug=args.debug)
