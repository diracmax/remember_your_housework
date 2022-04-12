from flask import Flask, render_template, request, flash, redirect
from cs50 import SQL
import datetime
import time
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SECRET_KEY"] = os.environ['SECRET_KEY']

db = SQL("sqlite:///project.db")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        is_error = False

        request_housework_name = request.form.get("housework_name")
        request_interval = request.form.get("interval")
        request_day_week_month = request.form.get("day_week_month")

        # Ensure housework_name was submitted
        if not request_housework_name:
            flash("Please input housework name!")
            is_error = True

        # Ensure interval was submitted
        if not request_interval:
            flash("Please input interval!")
            is_error = True

        # Store housework names in a list
        housework_names_queryset = db.execute(
            "SELECT housework_name FROM housework")
        housework_names = [housework_names_queryset[i]['housework_name']
                           for i in range(len(housework_names_queryset))]

        # Ensure the housework already exists
        if request_housework_name in housework_names:
            flash("The housework already exists!")
            is_error = True

        # Accept only positive numbers
        if not request_interval.isnumeric() or request_interval == 0:
            flash("Please input natural number!")
            is_error = True

        # Add the new housework
        if not is_error:
            db.execute("INSERT INTO housework (housework_name, interval, day_week_month) VALUES (?, ?, ?)",
                       request_housework_name, request_interval, request_day_week_month)

    # Get housework data
    housework_queryset = db.execute("SELECT * FROM housework")

    # Get Today's date
    today = datetime.date.today()

    for housework in housework_queryset:
        # Converts the last notification date to a date type
        time = datetime.datetime.strptime(
            housework["last_notification_date"], '%Y-%m-%d')
        time.isoformat()
        date = time.date()
        date.isoformat()

        # Calculate remaining days
        if housework["day_week_month"] == 'd':
            # "day" is selected
            housework["remaining_days"] = (
                date - today).days + housework["interval"]
        if housework["day_week_month"] == 'w':
            # "week" is selected
            housework["remaining_days"] = (
                date - today).days + housework["interval"] * 7
        if housework["day_week_month"] == 'm':
            # "month" is selected
            housework["remaining_days"] = (
                date - today).days + housework["interval"] * 31

        # Update the last notification day if notification.py isn't running
        if housework["remaining_days"] < 0:
            if housework["day_week_month"] == 'd':
                # "day" is selected
                housework["remaining_days"] = housework["interval"]
            if housework["day_week_month"] == 'w':
                # "week" is selected
                housework["remaining_days"] = housework["interval"] * 7
            if housework["day_week_month"] == 'm':
                # "month" is selected
                housework["remaining_days"] = housework["interval"] * 31

            db.execute("UPDATE housework SET last_notification_date = ? WHERE id = ?",
                       today, housework["id"])

            flash("I'm sorry. I may not have been able to notify you last time.")

        # interval for display
        if housework["day_week_month"] == 'd':
            # "day" is selected
            housework["interval_display"] = str(
                housework["interval"]) + " day"
        if housework["day_week_month"] == 'w':
            # "week" is selected
            housework["interval_display"] = str(
                housework["interval"]) + " week"
        if housework["day_week_month"] == 'm':
            # "month" is selected
            housework["interval_display"] = str(
                housework["interval"]) + " month"

    # Sort housework data by remaining days
    sorted_housework = sorted(
        housework, key=lambda x: x["remaining_days"])

    return render_template("index.html", housework_data=sorted_housework, today=today)


@app.route("/set", methods=["POST"])
def set_token():
    request_token = request.form.get("token")

    # Ensure LINE token was submitted
    if not request_token:
        flash("Please input LINE token!")
        return redirect("/")

    is_registerd = line(
        "Your LINE token has been successfully registered.", request_token)

    if is_registerd == 200:
        # Token is valid.
        token_data = db.execute("SELECT token FROM line_token")
        if len(token_data) == 0:
            db.execute("INSERT INTO line_token (token) VALUES (?)",
                       request_token)
        else:
            db.execute("UPDATE line_token SET token = ?",
                       request_token)

        flash("Your LINE token is registerd.")

    else:
        # Token is invalid.
        flash("This LINE token may be invalid. Please register again.")

    return redirect("/")


@app.route("/delete/<int:delete_id>")
def delete(delete_id):
    # Delete the row of the table "housework"
    db.execute("DELETE FROM housework WHERE id = ?", delete_id)
    flash("Deleted.")
    return redirect("/")


def line(message: str, token: str):
    # Send a message on LINE
    data = {'message': message}
    headers = {'Authorization': 'Bearer ' + token}
    res = requests.post(
        'https://notify-api.line.me/api/notify', data=data, headers=headers)
    return res.status_code
