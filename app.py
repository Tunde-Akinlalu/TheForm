import sqlite3
from flask import Flask, render_template, flash, request,redirect
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import csv
import pandas as pd
from sqlite3 import Error
import xlwt
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qiudata.db'
app.config['SECRET_KEY'] = 'pharma key'

# initialize the database
db = SQLAlchemy(app)

class patients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    input_date = db.Column(db.DateTime, default=datetime.today())
    emr = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(200), nullable=False)
    ward = db.Column(db.String(200), nullable=False)
    diagnosis = db.Column(db.String(200), nullable=False)
    operation = db.Column(db.String(200), nullable=False)
    specialty = db.Column(db.String(200), nullable=False)
    surgeon = db.Column(db.String(200), nullable=False)
    assistant = db.Column(db.String(200))
    scrub_nurse = db.Column(db.String(200))
    anaesthesia_type = db.Column(db.String(200), nullable=False)
    anaesthetist = db.Column(db.String(200), nullable=False)
    receiver = db.Column(db.String(200), nullable=False)
    pon = db.Column(db.String(200))
    amount_paid = db.Column(db.Integer, nullable=False)
    remark = db.Column(db.String(200))
    
 # Create a string
def __repr__(self):
    return '<Name %r>' % self.id

# Create a Form Class
class theatreform(FlaskForm):
    name = StringField("Patient Name", validators=[InputRequired()])
    emr = IntegerField("EMR", validators=[InputRequired()])
    age = IntegerField("Age", validators=[InputRequired()])
    gender = SelectField("Gender", choices=[('', ''), ('male', 'Male'), ('female', 'Female')],
                         validators=[InputRequired()])
    ward = SelectField("Ward", choices=[('', ''), ('vip', 'VIP'), ('general', 'General'), ('blue', 'Blue'),
                                        ('grey', 'Grey'), ('a&e', 'A & E'),
                                       ('maternity', 'Maternity'), ('ped', 'Paediatric'), ('silver', 'Silver'),
                                        ('neonatal', 'Neonatal'), ('epu', 'EPU')],
                       validators=[InputRequired()])
    diagnosis = StringField("Diagnosis", validators=[InputRequired()])
    operation = StringField("Operation", validators=[InputRequired()])
    specialty = SelectField("Specialty",
                                   choices=[('', ''), ('orthopaedics', 'Orthopaedics'), ('neuroSurgery', 'Neurosurgery'),
                                            ('gastroenterology', 'Gastroenterology'), ('Family_Medicine', 'Family Medicine'),
                                            ('o&g', 'O&G'), ('general_surgery', 'General Surgery'), ('urology', 'Urology'),
                                            ('paediatric', 'Paediatric'), ('ent', 'ENT'), ('plastic', 'Plastic'),
                                            ('maxillofacial', 'Maxillofacial'), ('ophthalmology', 'Ophthalmology'),
                                            ('nephrology', 'Nephrology'), ('cadiothoracic', 'Cadiothoracic'),
                                            ('dermatology', 'Dermatology'), ('paediatric_dermatology', 'Paediatric Dermaology'),
                                            ('kidney_transplant', 'Kidney Transplant')],
validators=[InputRequired()])
    surgeon = StringField("Surgeon", validators=[InputRequired()])
    assistant = StringField("Assistant")
    scrub_nurse = StringField("Scrub Nurse", validators=[DataRequired()])
    anaesthesia_type = SelectField("Anaesthesia Type",
                                   choices=[('', ''), ('local', 'Local'), ('general', 'General'),
                                            ('sedation', 'Sedation'), ('sab', 'SAB'), ('combined_spinal', 'Combined Spinal')],
                                   validators=[InputRequired()])
    anaesthetist = StringField("Anaesthetist", validators=[InputRequired()])
    receiver = StringField("Receiver")
    pon = StringField("PON")
    amount_paid = IntegerField("Amount Paid", validators=[InputRequired()])
    remark = TextAreaField("Remark")
    submit = SubmitField("Submit")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/create_form', methods=['GET', 'POST'])
def create_form():
    name = None
    emr = None
    age = None
    gender = None
    ward = None
    diagnosis = None
    operation = None
    specialty = None
    surgeon = None
    assistant = None
    scrub_nurse = None
    anaesthesia_type = None
    anaesthetist = None
    receiver = None
    pon = None
    amount_paid = None
    remark = None
    form = theatreform()
    # Validate Form
    if form.validate_on_submit():
        new_px = patients(name=form.name.data.upper(), emr=form.emr.data, age=form.age.data, gender=form.gender.data.upper(),
                              ward=form.ward.data.upper(), diagnosis=form.diagnosis.data.upper(), operation=form.operation.data.upper(),
                              specialty=form.specialty.data.upper(), surgeon=form.surgeon.data.upper(), assistant=form.assistant.data.upper(),
                              scrub_nurse=form.scrub_nurse.data.upper(), anaesthesia_type=form.anaesthesia_type.data.upper(),
                              anaesthetist=form.anaesthetist.data.upper(), receiver=form.receiver.data.upper(), pon=form.pon.data.upper(),
                            amount_paid=form.amount_paid.data, remark=form.remark.data.upper()
                            )
        db.session.add(new_px)
        db.session.commit()

        name = form.name.data
        form.name.data = ''

        emr = form.emr.data
        form.emr.data = ''

        age = form.age.data
        form.age.data = ''

        gender = form.gender.data
        form.gender.data = ''

        ward = form.ward.data
        form.ward.data = ''

        diagnosis = form.diagnosis.data
        form.diagnosis.data = ''

        operation = form.operation.data
        form.operation.data = ''

        specialty = form.specialty.data
        form.specialty.data = ''

        surgeon = form.surgeon.data
        form.surgeon.data = ''

        assistant = form.assistant.data
        form.assistant.data = ''

        scrub_nurse = form.scrub_nurse.data
        form.scrub_nurse.data = ''

        anaesthesia_type = form.anaesthesia_type.data
        form.anaesthesia_type.data = ''

        anaesthetist = form.anaesthetist.data
        form.anaesthetist.data = ''

        receiver = form.receiver.data
        form.receiver.data = ''

        pon = form.pon.data
        form.pon.data = ''

        amount_paid = form.amount_paid.data
        form.amount_paid.data = ''

        remark = form.remark.data
        form.remark.data = ''

        flash("Patient added successfully", "success")
        pxs = patients.query.order_by(patients.input_date)
    return render_template("create_form.html", name=name, emr=emr, age=age, gender=gender, ward=ward,
                           diagnosis=diagnosis, operation=operation, specialty=specialty, surgeon=surgeon,
                           assistant=assistant, scrub_nurse=scrub_nurse, anaesthesia_type=anaesthesia_type,
                           anaesthetist=anaesthetist, receiver=receiver, pon=pon, amount_paid=amount_paid,
                           remark=remark, form=form)

@app.route("/view")
def view():
 con = sqlite3.connect("qiudata.db")
 con.row_factory = sqlite3.Row
 cur = con.cursor()
 cur.execute("select * from patients order by input_date desc")
 rows = cur.fetchall()
 return render_template("view.html", rows=rows)

@app.route("/download_report")
def download_report():
    conn = sqlite3.connect("qiudata.db")
    cursor = conn.cursor()
    cursor.execute("select * from patients")
    with open("patients_data.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter="\t")
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)

        dirpath = os.getcwd() + "/patients_data.csv"
        flash("Data exported Successfully into {}".format(dirpath), "success")
        return render_template("download_report.html")
        conn.close()

#@app.route("/upload") ####### for future use
#def upload():
#    conn = sqlite3.connect('qiudata.db')
#    wb = pd.read_excel('patients_data.xlsx')
#    wb.to_sql(name='px_data', con=conn, if_exists='replace', index=True)
#    conn.commit()
#    return render_template("upload.html")
#    conn.close()





# Update
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    form=theatreform()
    patient_to_edit = patients.get  (id)
    if request.method == "POST":
       patient_to_edit.name = request.form['name']
       patient_to_edit.emr = request.form['emr']
       patient_to_edit.age = request.form['age']
       patient_to_edit.gender = request.form['gender']
       patient_to_edit.ward = request.form['ward']
       patient_to_edit.diagnosis = request.form['diagnosis']
       patient_to_edit.operation = request.form['operation']
       patient_to_edit.specialty = request.form['specialty']
       patient_to_edit.surgeon = request.form['surgeon']
       patient_to_edit. assistant = request.form.get('assistant', False)
       patient_to_edit.scrub_nurse = request.form['scrub_nurse']
       patient_to_edit.anaesthesia_type = request.form.get('anaesthesia_type', False)
       patient_to_edit.anaesthetist = request.form['anaesthetist']
       patient_to_edit.receiver = request.form.get('receiver', False)
       patient_to_edit.pon = request.form['pon']
       patient_to_edit.remark = request.form['remark']
    try:
        con = sqlite3.connect("qiudata.db")
        cur = con.cursor()
        cur.execute('UPDATE patients SET name = ?, emr = ?, age = ?, gender = ?, ward = ?, diagnosis = ?, '
                    'operation = ?, specialty = ?,surgeon = ?, assistant = ?, scrub_nurse = ?, '
                    'anaesthesia_type = ?, anaesthetist = ?, receiver = ?, pon = ?, remark = ?'
                     ' WHERE id = ?',
                    ("name", "emr", "age", "gender", "ward", "diagnosis", "operation", "special    ty", "surgeon",
                    "assistant", "scrub_nurse", "anaesthesia_type", "anaesthetist", "receiver", "pon",
                    "remark", "id"))
        flash("Patient details updated successfully!", "success")
        return redirect("view.html")
    except:
        flash("There was a problem updating patient details", "caution")
        return render_template("edit.html", form=form, patient_to_edit=patient_to_edit)

@app.route("/delete/<int:id>")
def delete(id):
    patient_to_delete = patients.query.get_or_404('id')
    name = None
    emr = None
    age = None
    gender = None
    ward = None
    diagnosis = None
    operation = None
    specialty = None
    surgeon = None
    assistant = None
    scrub_nurse = None
    anaesthesia_type = None
    anaesthetist = None
    receiver = None
    pon = None
    remark = None
    form = theatreform()

    try:
        db.session.delete(patient_to_delete)
        db.session.commit()
        flash("Patient Deleted Successfully!!!", "success")
        pxs = patients.query.order_by(patients.input_date)
        return render_template("view.html", name=name, emr=emr, age=age, gender=gender, ward=ward,
                               diagnosis=diagnosis, operation=operation, specialty=specialty, surgeon=surgeon,
                               assistant=assistant, scrub_nurse=scrub_nurse, anaesthesia_type=anaesthesia_type,
                               anaesthetist=anaesthetist, receiver=receiver, pon=pon, remark=remark,
                               form=form)
    except:
        flash("OOOOps!!! Patient Not Deleted")
        return render_template("view.html", name=name, emr=emr, age=age, gender=gender, ward=ward,
                               diagnosis=diagnosis, operation=operation, specialty=specialty, surgeon=surgeon,
                               assistant=assistant, scrub_nurse=scrub_nurse, anaesthesia_type=anaesthesia_type,
                               anaesthetist=anaesthetist, receiver=receiver, pon=pon, remark=remark,
                               form=form)

