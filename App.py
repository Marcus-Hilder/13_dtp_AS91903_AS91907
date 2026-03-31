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
    
    return render_template("index.html", page_title=page_title, active_page="index")

@app.route('/timetable')
def timetable():
    page_title = "Westlake Clubs | Timetable"

    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    week = request.args.get('week', type=int)
    today_param = request.args.get('today', type=int)  # new, for mobile day nav

    today_dt = datetime.now()
    if not year:
        year = today_dt.year
    if not month:
        month = today_dt.month

    cal = calendar.monthcalendar(year, month)

    # Prev/next month with year wraparound
    prev_month = 12 if month == 1 else month - 1
    prev_year  = year - 1 if month == 1 else year
    next_month = 1 if month == 12 else month + 1
    next_year  = year + 1 if month == 12 else year

    prev_week_count = len(calendar.monthcalendar(prev_year, prev_month)) - 1

    month_back    = calendar.monthcalendar(prev_year, prev_month)
    month_forward = calendar.monthcalendar(next_year, next_month)
    month_name    = calendar.month_name[month]

    # Determine active week
    if week is None:
        week = 0
        for i, for_week in enumerate(cal):
            if today_dt.day in for_week and month == today_dt.month and year == today_dt.year:
                week = i
                break

    cal_week = cal[week]

    # Determine active day
    if today_param and today_param in cal_week:
        today = today_param
    elif today_dt.day in cal_week and month == today_dt.month and year == today_dt.year:
        today = today_dt.day
    else:
        today = next((d for d in cal_week if d != 0), 0)

    conn = get_db_conn()
    conn.row_factory = sqlite3.Row
    club_all = conn.execute("SELECT * FROM clubs").fetchall()
    club_dic = {
        row["id"]: {
            "club_day":         int(row["club_day"]),
            "club_slot":        row["club_slot"],
            "club_name":        row["club_name"],
            "club_description": row["club_description"],
        }
        for row in club_all
    }

    return render_template(
        "timetable.html",
        page_title=page_title,
        cal=cal,
        cal_week=cal_week,
        week=week,
        month_name=month_name,
        month=month,
        year=year,
        prev_month=prev_month,
        prev_year=prev_year,
        next_month=next_month,
        next_year=next_year,
        prev_week_count=prev_week_count,
        month_back=month_back,
        month_forward=month_forward,
        club_dic=club_dic,
        today=today,
        active_page="timetable",
    )
 
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

        return render_template("sign_ups.html", page_title=page_title, clubs=clubs, active_page="sign_ups", submit=True)


    conn = get_db_conn()
    clubs = conn.execute('SELECT * FROM clubs ORDER BY club_name ASC').fetchall()
    conn.close()

    return render_template("sign_ups.html", page_title=page_title, clubs=clubs, active_page="sign_ups")

@app.route('/enquiries', methods=["GET", "POST"])
def enquiries():
    """Enquiries webpage"""
    page_title = "Westlake Clubs - Enquiries"

    if request.method == "POST":
        email = request.form.get("email").strip()
        enquiry = request.form.get("enquiry").strip()
        
        conn = get_db_conn()
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()
        cur.execute("INSERT INTO enquiries (email, enquiry) VALUES (?, ?)", (email, enquiry))
        conn.commit()
        conn.close()

        return render_template("enquiries.html", page_title=page_title, submit=True, active_page="enquiries")

    return render_template("enquiries.html", page_title=page_title, active_page="enquiries")



@app.route('/create_club')
def create_club():
    """Create club webpage"""
    page_title = "Westlake Clubs - Create Club"

    if request.method == "POST":
        full_name = request.form.get("full_name").strip()
        email = request.form.get("email").strip()
        description = request.form.get("description").strip()
        skills_desc = request.form.get("skills_desc").strip()
        days = request.form.get("days").strip()

        
        conn = get_db_conn()
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()
        cur.execute("INSERT INTO club_requests (full_name, email, description, skills_desc, days) VALUES (?, ?, ?, ?, ?)", (full_name, email, description, skills_desc, days))
        conn.commit()
        conn.close()

        return render_template("create_club.html", page_title=page_title, submit=True, active_page="create_club")

    return render_template("create_club.html", page_title=page_title, active_page="create_club")

@app.route('/review', methods=["GET", "POST"])
def review():
    """Review webpage"""
    conn = get_db_conn()
    clubs = conn.execute('SELECT * FROM clubs ORDER BY club_name ASC').fetchall()

    if request.method == "POST":
        
        reviewer_name = request.form.get("full_name")
        email = request.form.get("email")
        club = request.form.get("club")
        club_experince = request.form.get("club_experince")
        club_Rating = request.form.get("rating")
        cur = conn.cursor()
        
        for i in clubs:
            if i['club_name'] == club:
                club = i['id']
                break
        cur.execute("INSERT INTO club_review (reviewer_name, club_id, club_experince, club_Rating) VALUES (?, ?, ?, ?)",\
        (reviewer_name, club, club_experince, club_Rating))
        conn.commit()
        return render_template("review.html", page_title="Westlake Clubs - Review", clubs=clubs, active_page="review", submit=True)
    
    return render_template("review.html", page_title="Westlake Clubs - Review", active_page="review",clubs=clubs)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
