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
    page_title = "Home"
    """main home page """
    
    return render_template("index.html", page_title=page_title)

@app.route('/Marcus_test')
def marcus_test():
    """main home page """
    
    return render_template("index.html",)

