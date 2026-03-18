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
@app.route('/test')
def test():
    page_title = "test"
    
    
    return render_template("timetable2.html", page_title=page_title)
@app.route('/')
def index():
    page_title = "Home"
    """main home page """
    
    return render_template("index.html", page_title=page_title)

@app.route('/timetable')
def timetable():
    page_title = "Westlake Clubs | Timetable"
    # Get year/month from URL params or default to today
    year = None #0000 - 9999
    month = None #1 - 12
    week = None #0 - 6
    
    today_dt = datetime.now()
    if not year:
        year = today_dt.year  
    if not month:
        month = today_dt.month
    if not week:
        week_count = 0
        today_week = 0
        # if in curent month then set week to today else defalt to the first week.
        
    cal = calendar.monthcalendar(year, month)
    for week in cal:
            for day in week:
                if day == today_dt.day and month == today_dt.month:
                    today_week = week_count
            week_count += 1
    # get the cal for the wanted week
    cal_week = cal[today_week]
    month_back = calendar.monthcalendar(year, month -1)
    month_forward = calendar.monthcalendar(year, month +1)
    month_name = calendar.month_name[month]
    conn = get_db_conn()
    
    
    
    

    # club pull and write to dict
    conn.row_factory = sqlite3.Row
    check = conn.execute("SELECT * FROM clubs")
    club_all = check.fetchall()
    club_dic = {}
    for day in club_all:
        club_dic[day["id"]] = {}
        club_dic[day["id"]]["club_day"] = int(day["club_day"])
        club_dic[day["id"]]["club_slot"] = int(day["club_slot"])
        club_dic[day["id"]]["club_name"] = day["club_name"]
        club_dic[day["id"]]["club_description"] = day["club_description"]
    # for i, items in club_dic.items():
    #     if items["club_day"] == 1:
    #         print(items)




    return render_template("timetable2.html",page_title=page_title,cal=cal,cal_week=cal_week,month_name=month_name,club_dic=club_dic)

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
        clubs = conn.execute('SELECT * FROM clubs ORDER BY club_name ASC').fetchall()

        cur = conn.cursor()
        cur.execute("INSERT INTO signups (full_name, email, club, why_desc, availability_desc) VALUES (?, ?, ?, ?, ?)", (full_name, email, club, why_desc, availability_desc))
        conn.commit()
        conn.close()

        return render_template("sign_ups.html", page_title=page_title, clubs=clubs)


    conn = get_db_conn()
    clubs = conn.execute('SELECT * FROM clubs ORDER BY club_name ASC').fetchall()
    conn.close()

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
    app.run(debug=True, port=8080)
