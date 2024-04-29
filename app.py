from audioop import add
import re
import sys
import argparse
from flask import Flask, render_template, url_for, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from sqlalchemy import text
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask_caching import Cache
from api.financial_data import EODHDAPIsDataFetcher
from config import API_TOKEN, ENABLE_RATE_LIMITING_PER_USER, ENABLE_REMOTE_CODE_MITIGATION, ENABLE_SAFE_SECRETS, ENABLE_HTTPS
from utils import validate_input, validate_password, validate_username
from sqlalchemy_utils import EncryptedType
from cryptography.fernet import Fernet

from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address

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

encryption_key = b'DZ1kh-bNO3VPqwTJxzp8NBdvg8zDVYw3crNJVURNXwM=' 

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

if ENABLE_RATE_LIMITING_PER_USER:
    limiter = Limiter(app=app, key_func=lambda: current_user,
                      default_limits=["1 per second"])

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'this is a secret key '
app.config['CACHE_TYPE'] = 'simple'
db = SQLAlchemy(app)
cache = Cache(app)

if ENABLE_SAFE_SECRETS:
    bcrypt = Bcrypt(app)

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    if ENABLE_SAFE_SECRETS:
        ssn = db.Column(EncryptedType(db.String, encryption_key), nullable=False)
    else:
        ssn = db.Column(db.String(80), nullable=False)
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
@login_required
@cache.cached(timeout=5)
def welcome():
    exchanges = data_fetcher.fetch_exchanges()
    return render_template("exchanges.html", exchanges=exchanges, name=current_user.username)


@app.route("/exchange/<code>")
@login_required
@cache.cached(timeout=5)
def exchange_markets(code):
    markets = data_fetcher.fetch_exchange_markets(code)
    return render_template("markets.html", code=code, markets=markets, name=current_user.username)

@app.route('/exchange/about')
def about():
    print("Rendering about.html")
    return render_template('about.html')  # Render the "about.html" template

@app.route("/exchange/<code>/<market>/<granularity>")
@login_required
@cache.cached(timeout=5)
def exchange_market_data(code, market, granularity):
    candles = data_fetcher.fetch_exchange_market_data(
        code, market, granularity)
    return render_template("data.html", code=code, market=market, granularity=granularity, candles=candles, name=current_user.username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = validate_username(request.form['username'])
            password = validate_password(request.form['password'])
        except Exception as e:
            return render_template('login.html', error=e), 401 #Unauthorized

        # Validate if user exists
        if not ENABLE_REMOTE_CODE_MITIGATION:
            raw_sql_query = text(f"SELECT * FROM user WHERE username = '{username}'")
            with db.engine.connect() as conn:
                result = conn.execute(raw_sql_query)
                rows = result.fetchall()
                if len(rows) != 1:
                    error = f"Invalid username or password: ErrorDetails: {rows}"
                    return render_template('login.html', error=error), 401 #Unauthorized

        user = User.query.filter_by(username=username).first()
        if ENABLE_SAFE_SECRETS and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('welcome'))
        elif not ENABLE_SAFE_SECRETS and user.password == password:
            login_user(user)
            return redirect(url_for('welcome'))
        else:
            error = 'Invalid username or password.'
            return render_template('login.html', error=error), 401 #Unauthorized

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = validate_username(request.form['username'])
            password = validate_password(request.form['password'])
            if ENABLE_SAFE_SECRETS:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') 
            else:
                hashed_password = password
            address = validate_input(request.form['address'])
            phone = validate_input(request.form['phone'])
            ssn = validate_input(request.form['ssn'])
        except Exception as e:
            return render_template('registration.html', error=e), 401 #Unauthorized

        if ENABLE_SAFE_SECRETS:
            cipher_suite = Fernet(encryption_key)
            new_user_ssn = cipher_suite.encrypt(bytes(ssn, encoding='utf8'))
        else:
            new_user_ssn = ssn

        new_user = User(username=username, password=hashed_password,
                        address=address, phone=phone, ssn=new_user_ssn)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('registration.html')


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
    if ENABLE_HTTPS    :
        app.run(host=http_host, port=http_port, threaded=True, ssl_context=('cert.pem', 'key.pem'))
    else:
        app.run(host=http_host, port=http_port, threaded=True)
