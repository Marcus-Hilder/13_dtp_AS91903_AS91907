from flask import Flask, render_template,request, redirect, url_for
import sqlite3

app = Flask(__name__) 

def get_db_conn():
    """setup connection to sql database"""
    conn = sqlite3.connect('INPUT HERE.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """main home page """
    
    return render_template("index.html",)

@app.route('/Marcus_test')
def marcus_test():
    """main home page """
    
    return render_template("index.html",)

@app.route('/sign_ups')
def sign_ups():
    """Sign ups webpage"""
    page_title = "Westlake Clubs - Sign Ups"

    return render_template("sign_ups.html", page_title=page_title)
