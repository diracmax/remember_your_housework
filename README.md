# Remember your HOUSEWORK!
#### Video Demo:  <https://www.youtube.com/watch?v=qpf1HRq28tw>
#### Description:

This is an application that notifies you of houseworks that you may have forgotten to do, using an application called LINE.

LINE is a messaging application used by a very large number of people in Japan.

Many people will receive their notifications smoothly because of LINE.

##### Features

We designed it so that users can do their housework without forgetting.

The application LINE, commonly used in Japan, makes it easy for users to check their notifications.

We created this site for personal use, so there is no login.

The application will show you the housework you have registered, in order of the number of remaining days.

I have designed a simple UI to make it easy for users to use.

I used more bootstrap than css.

##### Languages and Technologies

HTML CSS JavaScript Bootstrap Python

##### Web framework

Flask

##### Explanation for each files

templates/index.html
This is the HTML file that displays the main content.

templates/layout.html
Page template. Here I am importing the files in the directory "static".

static/script.js
This JavaScript file is used to colour the numbers when the number of remaining days is low.

static/style.css
This is just a CSS file to change the colour of the delito button.

application.py
Within this file, you can register houseworks, erase houseworks and set tokens.

notification.py
This is a program to send periodic notifications to users. It has no direct dependency on application.py.

project.db
This file has the tables "line_token" and "housework".
As this is for personal use, the application.py is designed so that no more than one token can be stored.

README.md
This file

requirement.txt
It describes the external modules this application need.

##### Requirement

cs50
flask

##### Installation

```bash
pip3 install cs50
pip install Flask
```

##### Usage

```bash
docker-compose up
```

When you access the indicated URL, the application will display.

Always run /project/notification.py in order to notify.

```bash
python3 notification.py
```

First, you need to register your LINE access token. If the token is set correctly, LINE will notify you of that.

You need to register the name of houseworks and the interval.

You will receive notifications on LINE every period.

If the interval is weekly or monthly, you will also be notified the day before or the day after the appointment.

##### Technical challenges

We used an API called LINE Notify API. Using this, you can send notifications to the talk room and perform authentication.

I used python's schedule module to make the function run periodically.

##### Note

Please visit this site to obtain your LINE access token. [LINE Notify](https://notify-bot.line.me/ja/)

You must be a registered LINE member.

There is no dependency between application.py and notification.py. They share project.db.

##### Nickname

* Nickname: Diracma

##### Last message

In the future, I will use CRON to run the notification.py at regular intervals, and I will also create a line bot.

I also want to migrate this application onto a real server.

That's it. Thank you for reading README very much.