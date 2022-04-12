from cs50 import SQL
import datetime
import schedule
import time
import requests


db = SQL("sqlite:///project.db")


def line(message: str, token: str):
    # Send a message on LINE
    data = {'message': message}
    headers = {'Authorization': 'Bearer ' + token}
    res = requests.post(
        'https://notify-api.line.me/api/notify', data=data, headers=headers)


def regular_notifications():
    housework_data = db.execute("SELECT * FROM housework")

    # Get Today's date
    today = datetime.date.today()

    # Notify me if it's the notification
    for housework_datum in housework_data:
        # Converts the last notification date to a date type
        tdatetime = datetime.datetime.strptime(
            housework_datum["last_notification_date"], '%Y-%m-%d')
        last_notification_date = datetime.date(
            tdatetime.year, tdatetime.month, tdatetime.day)

        # Set notification date
        if housework_datum["day_week_month"] == 'd':
            reservation_date = last_notification_date + \
                datetime.timedelta(days=housework_datum["interval"])

        elif housework_datum["day_week_month"] == 'w':
            reservation_date = last_notification_date + \
                datetime.timedelta(days=housework_datum["interval"] * 7)

        elif housework_datum["day_week_month"] == 'm':
            reservation_date = housework_datum["last_notification_date"] + \
                datetime.timedelta(days=housework_datum["interval"] * 31)

        token_data = db.execute("SELECT token FROM line_token")

        # Exist access token
        if len(token_data) != 0:
            # Notify if today is the day before the reservation day.
            if today == reservation_date - datetime.timedelta(days=1):
                # Notify when "week" or "month" are registerd.
                if housework_datum["day_week_month"] == 'w' or housework_datum["day_week_month"] == 'm':
                    line('Please do {} tomorrow!'.format(
                        housework_datum["housework_name"]), token_data[0]["token"])

            # Notify if today is the reservation day.
            elif today == reservation_date:
                line('Please do {} !'.format(
                    housework_datum["housework_name"]), token_data[0]["token"])
                # Update last notification date if "day" is registerd
                if housework_datum["day_week_month"] == 'd':
                    db.execute("UPDATE housework SET last_notification_date = ? WHERE id = ?;",
                               reservation_date, housework_datum["id"])

            # Notify if today is the day after the reservation day.
            elif today == reservation_date + datetime.timedelta(days=1):
                if housework_datum["day_week_month"] == 'w' or housework_datum["day_week_month"] == 'm':
                    line('Did you do {} the day before? If you have not done that, you should do right now!'.format(
                        housework_datum["housework_name"]), token_data[0]["token"])
                    # Update last notification date when "week" or "month" are registerd.
                    db.execute("UPDATE housework SET last_notification_date = ? WHERE id = ?;",
                               reservation_date + datetime.timedelta(days=1), housework_datum["id"])


# Scheduling to run at 10am
schedule.every().day.at("07:59").do(regular_notifications)

while True:
    schedule.run_pending()
    time.sleep(60)
