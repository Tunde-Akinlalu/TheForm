import sqlite3
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# app = Flask(__name__)
# app.config['SECRET_KEY'] = "bosfay@100%"
# Old SQLite
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qiudata.db'

# initialize the database
# db = SQLAlchemy(app)


# After the above, go to the terminal, type (1) python; (2) from app (the main python file) import db;
# (3) db.create_all()
# view = []

con = sqlite3.connect('database.db')

cursor = con.cursor()

sql_query = """
create table if not exists theatre (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name CHAR NOT NULL,
                   input_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                   emr INTEGER NOT NULL,
                   age CHAR NOT NULL,
                   gender CHAR NOT NULL,
                   ward CHAR NOT NULL,
                   diagnosis CHAR NOT NULL,
                   operation CHAR NOT NULL,
                   specialty CHAR NOT NULL,
                   surgeon CHAR NOT NULL,
                   assistant CHAR NOT NULL,
                   scrub_nurse CHAR NULL,
                   anaesthesia_type CHAR NOT NULL,
                   anaesthetist CHAR NOT NULL,
                   receiver CHAR NULL,
                   pon CHAR NOT NULL,
                   remark CHAR)
"""
# with open('schema') as f:
#    connection.executescript(f.read())
#cursor.execute(sql_query)

#cursor.execute("INSERT INTO theatre (name, input_date, emr, age, gender, ward, diagnosis, "
 #              "operation, specialty, surgeon, assistant, scrub_nurse, anaesthesia_type, anaesthetist, "
 #                "receiver, pon, remark)"
 #              " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
 #              ("Patient Name", "Date", "EMR", "Age", "Gender", "Ward", "Diagnosis", "Operation", "Specialty",
  #              "Surgeon", "Assisting Surgeon", "Scrub Nurse", "Type of Anaesthesia", "Anaesthetist",
   #             "Sample Receiver", "PON", "Remark")
    #           )
con.commit()
con.close()

# cur = db.cursor()


# db.commit()
# db.close()
