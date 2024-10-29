# scraper-challenge
A tool that takes a website URL as input, scrapes its content, and classifies visitors based on their interests or industry. Part of a data pipeline to dynamically generate questions and multiple-choice options that help categorize users visiting the site.

### Requirements:
Tech stack must be Frontend: React, Redux | Backend & Cloud: Python, Flask, AWS

### Quickstart
It is recommended to run this locally in a virtual env. Run `. venv .venv`.

To run the Flask app, run `flask --app app run --debug` in your command line.

To run the file that confirms we can connect to mongodb, first create an `.env` file in the root directory:
```
SCRAPER_APP_CONNECTION_STRING=<your-connection-string>
```
Then simply run `python3 app/db.py`.