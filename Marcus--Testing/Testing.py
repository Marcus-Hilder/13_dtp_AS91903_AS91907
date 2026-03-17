from flask import Flask, render_template,request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta
import calendar

def get_db_conn():
    """setup connection to sql database"""
    conn = sqlite3.connect('club_data.db')
    conn.row_factory = sqlite3.Row
    return conn

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
    club_all = check.fetchall()
    club_dic = {}
    
    for day in club_all:
        club_name = day["club_name"] 
        club_dic[day["id"]] = {}
        club_dic[day["id"]]["club_day"] = int(day["club_day"])
        club_dic[day["id"]]["club_name"] = club_name
        club_dic[day["id"]]["club_description"] = day["club_description"]
    for i, a in club_dic.items():
        print(i, ":",a)

timetable()