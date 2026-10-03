from flask import Flask, render_template, request, redirect, session
import sqlite3
from model import predict_credit

app = Flask(__name__)
app.secret_key = "agriculture_loan_secret_key"


# ---------------- DATABASE ----------------

def get_db():
    conn = sqlite3.connect(
        "database.db",
        timeout=10
    )
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


create_tables()


# ---------------- HOME ----------------

@app.route("/")
def index():
    return render_template("index.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        try:

            conn = get_db()

            conn.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password)
            )

            conn.commit()
            conn.close()

            return redirect("/login")

        except sqlite3.IntegrityError:

            return "Email already registered!"

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()

        conn.close()

        if user:

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            return redirect("/dashboard")

        return "Invalid email or password!"

    return render_template("login.html")


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        name=session["user_name"]
    )


# ---------------- CREDIT SCORE ----------------

@app.route("/predict", methods=["POST"])
def predict():

    if "user_id" not in session:
        return redirect("/login")

    land_size = float(request.form["land_size"])
    annual_income = float(request.form["annual_income"])
    existing_loan = float(request.form["existing_loan"])
    repayment_history = float(request.form["repayment_history"])
    crop_success = float(request.form["crop_success"])
    weather_risk = float(request.form["weather_risk"])

    prediction, score, risk = predict_credit(
        land_size,
        annual_income,
        existing_loan,
        repayment_history,
        crop_success,
        weather_risk
    )

    if prediction == 1:
        status = "Loan Likely Approved"
    else:
        status = "Loan Requires Further Review"

    factors = []

    if annual_income < 250000:
        factors.append("Low annual income")

    if existing_loan > 300000:
        factors.append("High existing loan")

    if repayment_history < 5:
        factors.append("Weak repayment history")

    if crop_success < 5:
        factors.append("Low crop success rate")

    if weather_risk > 7:
        factors.append("High weather risk")

    if len(factors) == 0:
        factors.append("Good financial and agricultural indicators")

    return render_template(
        "result.html",
        score=score,
        risk=risk,
        status=status,
        factors=factors
    )


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=False)