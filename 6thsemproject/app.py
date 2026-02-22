from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.user import User

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# ---------------- User Registration ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if User.get_by_email(email):
            flash("Email already registered!", "danger")
            return redirect(url_for("register"))

        user = User(name, email, password, role="user")
        user.save()
        flash("User registration successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("user/register.html")

# ---------------- Admin Registration ----------------
@app.route("/admin/register", methods=["GET", "POST"])
def admin_register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if User.get_by_email(email):
            flash("Email already registered!", "danger")
            return redirect(url_for("admin_register"))

        admin = User(name, email, password, role="admin")
        admin.save()
        flash("Admin registration successful! Please login.", "success")
        return redirect(url_for("admin_login"))

    return render_template("admin/register.html")

# ---------------- User Login ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.verify_password(email, password)
        if user:
            if user['role'] == 'user':
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                flash("Welcome, " + user['name'], "success")
                return redirect(url_for("user_dashboard"))
            else:
                flash("You are not a user!", "danger")
                return redirect(url_for("login"))
        else:
            flash("Invalid credentials!", "danger")
            return redirect(url_for("login"))

    return render_template("user/login.html")

# ---------------- Admin Login ----------------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.verify_password(email, password)
        if user:
            if user['role'] == 'admin':
                session['admin_id'] = user['id']
                session['admin_name'] = user['name']
                flash("Welcome Admin!", "success")
                return redirect(url_for("admin_dashboard"))
            else:
                flash("You are not an admin!", "danger")
                return redirect(url_for("admin_login"))
        else:
            flash("Invalid credentials!", "danger")
            return redirect(url_for("admin_login"))

    return render_template("admin/login.html")