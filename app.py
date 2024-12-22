from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets
import pymysql
import os


# First, create the database if it doesn't exist
def create_database():
    try:
        connection = pymysql.connect(
            host="crypto.cnuaa2aqad3k.eu-north-1.rds.amazonaws.com",
            user="admin",
            password="Omer1708",
            port=3306,
        )
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS crypto")
        connection.close()
        print("Database 'crypto' created or already exists.")
    except Exception as e:
        print(f"Error creating database: {e}")
        raise


# Create database before Flask app initialization
create_database()

# Replace PostgreSQL driver with MySQL driver
pymysql.install_as_MySQLdb()

app = Flask(__name__)

secret_key = os.getenv("SECRET_KEY", None)
if not secret_key:
    raise ValueError("SECRET_KEY is not set in the environment variables!")
app.config["SECRET_KEY"] = secret_key

# Database configuration
DB_USER = os.getenv("DB_USER", "default_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "default_password")
DB_NAME = os.getenv("DB_NAME", "default_db_name")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")

# # Database configuration
# DB_USER = "admin"
# DB_PASSWORD = "Omer1708"
# DB_NAME = "crypto"
# DB_HOST = "crypto.cnuaa2aqad3k.eu-north-1.rds.amazonaws.com"
# DB_PORT = "3306"


@app.route('/googlefe12fb47c2daf00a.html')
def google_verification():
    return app.send_static_file('googlefe12fb47c2daf00a.html')


# Configure Flask app
app.config["SECRET_KEY"] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

print(f"Attempting to connect to database at: {DB_HOST}")

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Flask-Migrate integration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

print("Successfully initialized Flask-SQLAlchemy, Flask-Migrate, and LoginManager")


# Database Models
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    trades = db.relationship("Trade", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Trade(db.Model):
    __tablename__ = "trades"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    symbol = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    current_price = db.Column(db.DECIMAL(10, 6), nullable=False)
    risk_amount = db.Column(db.DECIMAL(10, 2), nullable=False)
    portfolio_risk = db.Column(db.DECIMAL(5, 2))
    take_profit_price = db.Column(db.DECIMAL(10, 6))
    stop_loss_price = db.Column(db.DECIMAL(10, 6))
    position_size = db.Column(db.DECIMAL(10, 6), nullable=False)
    potential_profit = db.Column(db.DECIMAL(10, 2))
    potential_loss = db.Column(db.DECIMAL(10, 2))
    risk_reward_ratio = db.Column(db.DECIMAL(5, 2))
    active = db.Column(db.Boolean, default=True)
    position_type = db.Column(
        db.String(10), nullable=False
    )  # New column for "long" or "short"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Routes
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 400

        user = User(email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        return jsonify({"success": True})

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return jsonify({"success": True})

        return jsonify({"error": "Invalid credentials"}), 401

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def home():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
@login_required
def calculate():
    try:
        data = request.form

        # Input Parsing
        symbol = data.get("symbol", "").strip()
        current_price = float(data.get("currentPrice", 0))
        position_type = data.get("positionType", "").lower()
        risk_amount = float(data.get("riskAmount", 0))
        stop_loss = float(data.get("stopLoss", 0)) if data.get("stopLoss") else None
        take_profit = (
            float(data.get("takeProfit", 0)) if data.get("takeProfit") else None
        )

        # Validation
        if not symbol or not position_type or not risk_amount:
            return jsonify({"error": "Missing required fields"}), 400
        if position_type not in ["long", "short"]:
            return jsonify({"error": "Invalid position type"}), 400
        if risk_amount <= 0 or current_price <= 0:
            return (
                jsonify(
                    {"error": "Risk amount and current price must be greater than zero"}
                ),
                400,
            )
        if stop_loss and abs(current_price - stop_loss) <= 0:
            return jsonify({"error": "Stop loss must not equal the current price"}), 400

        # Position Size Calculation
        if stop_loss:
            price_diff_for_loss = (
                current_price - stop_loss
                if position_type == "long"
                else stop_loss - current_price
            )
            if price_diff_for_loss <= 0:
                return (
                    jsonify(
                        {"error": "Invalid stop loss for the selected position type"}
                    ),
                    400,
                )
            position_size = risk_amount / abs(price_diff_for_loss)
        else:
            position_size = risk_amount / (current_price * 0.01)

        position_size = round(position_size, 6)

        # Potential Profit and Loss Calculation
        potential_profit = None
        potential_loss = None

        if position_type == "long":
            potential_profit = (
                position_size * (take_profit - current_price) if take_profit else None
            )
            potential_loss = (
                position_size * (current_price - stop_loss) if stop_loss else None
            )
        elif position_type == "short":
            potential_profit = (
                position_size * (current_price - take_profit) if take_profit else None
            )
            potential_loss = (
                position_size * (stop_loss - current_price) if stop_loss else None
            )

        # Round results
        potential_profit = (
            round(potential_profit, 2) if potential_profit is not None else None
        )
        potential_loss = (
            round(potential_loss, 2) if potential_loss is not None else None
        )
        risk_reward_ratio = (
            round(abs(potential_profit / potential_loss), 2)
            if potential_profit and potential_loss
            else None
        )

        # Save trade
        trade = Trade(
            user_id=current_user.id,
            symbol=symbol,
            current_price=current_price,
            risk_amount=risk_amount,
            stop_loss_price=stop_loss,
            take_profit_price=take_profit,
            position_size=position_size,
            potential_profit=potential_profit,
            potential_loss=potential_loss,
            risk_reward_ratio=risk_reward_ratio,
            position_type=position_type,
            active=True,
        )
        db.session.add(trade)
        db.session.commit()

        return jsonify(
            {
                "trade_id": trade.id,
                "position_type": position_type,
                "position_size": position_size,
                "potential_profit": potential_profit,
                "potential_loss": potential_loss,
                "risk_reward_ratio": risk_reward_ratio,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "entry_price": current_price,
            }
        )

    except Exception as e:
        print(f"Error in calculate: {e}")
        return jsonify({"error": "Calculation failed"}), 500


@app.route("/trades")
@login_required
def get_trades():
    try:
        trades = (
            Trade.query.filter_by(user_id=current_user.id, active=True)
            .order_by(Trade.date.desc())
            .all()
        )
        return jsonify(
            [
                {
                    "id": trade.id,
                    "symbol": trade.symbol,
                    "position_type": trade.position_type,
                    "entry_price": float(trade.current_price),
                    "stop_loss_price": (
                        float(trade.stop_loss_price) if trade.stop_loss_price else None
                    ),
                    "take_profit_price": (
                        float(trade.take_profit_price)
                        if trade.take_profit_price
                        else None
                    ),
                    "position_size": float(trade.position_size),
                    "potential_profit": (
                        float(trade.potential_profit)
                        if trade.potential_profit
                        else None
                    ),
                    "potential_loss": (
                        float(trade.potential_loss) if trade.potential_loss else None
                    ),
                    "risk_reward_ratio": (
                        float(trade.risk_reward_ratio)
                        if trade.risk_reward_ratio
                        else None
                    ),
                    "percentage_change": (
                        (
                            (
                                (trade.current_price - trade.current_price)
                                / trade.current_price
                            )
                            * 100
                        )
                        if trade.current_price
                        else None
                    ),  # Update with live data for current price
                }
                for trade in trades
            ]
        )
    except Exception as e:
        print(f"Error in get_trades: {e}")
        return jsonify({"error": "Failed to fetch trades"}), 500


@app.route("/trade/<int:trade_id>", methods=["DELETE"])
@login_required
def delete_trade(trade_id):
    try:
        trade = Trade.query.filter_by(id=trade_id, user_id=current_user.id).first()

        if trade:
            db.session.delete(trade)
            db.session.commit()
            return jsonify({"success": True})

        return jsonify({"error": "Trade not found"}), 404
    except Exception as e:
        print(f"Error in delete_trade: {e}")
        return jsonify({"error": "Failed to delete trade"}), 500


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    try:
        print("Starting Flask application...")

        # Test database connection first
        with app.app_context():
            db.engine.connect()
            print("Database connection successful!")

    except Exception as e:
        # If the database connection fails, print an error and exit
        print(f"Database connection failed: {e}")
        exit(1)

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        print("Tables created successfully!")

    # Run the application
    app.run(host="0.0.0.0", port=5000, debug=True)
