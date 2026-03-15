from flask import Flask, render_template,request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta
import calendar

def cal_test():
    # year = request.args.get('year', type=int)
    # month = request.args.get('month', type=int)
    year = None
    month = None
    today_dt = datetime.now()

    if not year:
        year = today_dt.year  
    if not month:
        month = today_dt.month
    cal = calendar.monthcalendar(year, month)
    for week in cal:
        for day in week:
             print(day)
                

cal_test()