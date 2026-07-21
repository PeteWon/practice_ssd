from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

def meets_password_requirements(password):
    # OWASP C6 (Level 1, no MFA): minimum 10 characters, no composition rules,
    # all printable ASCII + space accepted (no character restrictions imposed)
    if len(password) < 10:
        return False
    return True

COMMON_PASSWORDS_FILE = os.path.join(os.path.dirname(__file__), "10-million-password-list-top-1000.txt")

def load_common_passwords():
    with open(COMMON_PASSWORDS_FILE, "r", encoding="utf-8", errors="ignore") as f:
        return set(line.strip() for line in f if line.strip())

COMMON_PASSWORDS = load_common_passwords()

def is_common_password(password):
    return password in COMMON_PASSWORDS

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        password = request.form.get("password", "")
        if not meets_password_requirements(password):
            return render_template("index.html", error="Password must be at least 10 characters long.")
        if is_common_password(password):
            return render_template("index.html", error="This password is too common. Please choose another.")
        return redirect(url_for("welcome", password=password))
    return render_template("index.html")

@app.route("/welcome")
def welcome():
    password = request.args.get("password", "")
    if not meets_password_requirements(password) or is_common_password(password):
        return redirect(url_for("home"))
    return render_template("welcome.html", password=password)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)