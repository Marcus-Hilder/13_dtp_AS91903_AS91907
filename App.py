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

@app.route('/timetable')
def timetable():
    page_title = "Westlake Clubs | Timetable"
    # Get year/month from URL params or default to today
    year = None
    month = None
    
    today_dt = datetime.now()
    if not year:
        year = today_dt.year  
    if not month:
        month = today_dt.month
    cal = calendar.monthcalendar(year, month)
    month_back = calendar.monthcalendar(year, month -1)
    month_forward = calendar.monthcalendar(year, month +1)
    month_name = calendar.month_name[month]
    conn = get_db_conn()
    conn.row_factory = sqlite3.Row
    check = conn.execute("SELECT * FROM clubs")
    club = check.fetchall()
    for start in club:
        start_date = int(start["club_start_date"].split("-")[2])
        # print(start_date)
        # print(start["club_start_date"])
    

    return render_template("timetable.html",page_title=page_title,cal=cal,month_name=month_name)

@app.route('/sign_ups', methods=["GET", "POST"])
def sign_ups():
    """Sign ups webpage"""
    page_title = "Westlake Clubs | Sign Ups"

    if request.method == "POST":
        full_name = request.form.get("full_name").strip()
        email = request.form.get("email").strip()
        club = request.form.get("club").strip()
        why_desc = request.form.get("why_desc").strip()
        availability_desc = request.form.get("availability_desc").strip()
        
        conn = get_db_conn()
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()
        cur.execute("INSERT INTO signups VALUES (?, ?, ?, ?, ?)", (full_name, email, club, why_desc, availability_desc))
        conn.commit()
        conn.close()

        return render_template("sign_ups.html", page_title=page_title, clubs=clubs)


    conn = get_db_conn()
    clubs = conn.execute('SELECT * FROM clubs ORDER BY club_name ASC').fetchall()
    return render_template("sign_ups.html", page_title=page_title, clubs=clubs)

@app.route('/enquiries')
def enquiries():
    """Enquiries webpage"""
    page_title = "Westlake Clubs - Sign Ups"

    return render_template("enquiries.html", page_title=page_title)



@app.route('/create_club')
def create_club():
    """Create club webpage"""
    page_title = "Westlake Clubs - Create Club"

    return render_template("create_club.html", page_title=page_title)

@app.route('/review')
def review():
    """Review webpage"""
    page_title = "Westlake Clubs - Review"

    return render_template("review.html", page_title=page_title)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)