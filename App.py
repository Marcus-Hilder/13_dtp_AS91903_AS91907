from flask import Flask, render_template,request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta
import calendar

app = Flask(__name__) 

def get_db_conn():
    """setup connection to sql database"""
    conn = sqlite3.connect('club_data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    page_title = "Home"
    """main home page """
    
    return render_template("index.html", page_title=page_title)

@app.route('/TimeTable')
def TimeTable():
    page_title = "Westlake Clubs | Time Table"
    # Get year/month from URL params or default to today
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    today_dt = datetime.now()

    if not year or not month:
        year = today_dt.year
        month = today_dt.month
    cal = calendar.monthcalendar(year, month)

    conn = get_db_conn()
    conn.row_factory = sqlite3.Row
    check = conn.execute("SELECT * FROM clubs")
    club = check.fetchall()
    for i in club:
        print(i["club_start_date"])
    return render_template("timetable.html",page_title=page_title,calendar=cal,)

@app.route('/sign_ups')
def sign_ups():
    """Sign ups webpage"""
    page_title = "Westlake Clubs | Sign Ups"

    return render_template("sign_ups.html", page_title=page_title)

if __name__ == '__main__':
    app.run(debug=True, port=5000)