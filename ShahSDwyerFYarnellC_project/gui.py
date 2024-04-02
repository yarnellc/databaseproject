#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 18:11:42 2023

@author: faithdwyer chloeyarnell
"""

import tkinter as tk
import pymysql


def check_login():
    username = uentry.get()
    password = pentry.get()
    try:
        cnx = pymysql.connect(host='localhost', user=username, password=password, db='universityhealthservices',
                              charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

        mbutton = tk.Button(text="Check patId", command=lambda: check_patid(entry.get()))
        mbutton.pack()

    except pymysql.err.OperationalError as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


def check_patid(entry):
    username = uentry.get()
    password = pentry.get()
    cnx = pymysql.connect(host='localhost', user=username, password=password, db='universityhealthservices')

    # start cursor for idNum from patients
    cur = cnx.cursor()
    cur.execute('SELECT idNum FROM Patients')
    rows = cur.fetchall()  # store the tuples
    cnx.close()

    # initialize an empty list to store the idNums
    patient_info = []
    for (idNum,) in rows:
        patient_info.append(idNum)

    if int(entry) in patient_info:
        label2 = tk.Label(text='Would you like to see your health center, appointment(s), or bill(s)? \n'
                               'Type health center, appointments, or bills: ')
        label2.pack()
        entry4 = tk.Entry(width=50)
        entry4.pack()
        button5 = tk.Button(text="submit", command=lambda: patient_sud(entry4.get(), entry))
        button5.pack()
    else:
        label2 = tk.Label(text='Invalid patient idNum. Please check and try again with your correct id. ')
        label2.pack()
        entry2 = tk.Entry(width=50)
        entry2.pack()
        button3 = tk.Button(text="submit", command=lambda: check_patid(entry2.get()))
        button3.pack()


def patient_sud(entry4, entry):
    if entry4 == "health center":
        username = uentry.get()
        password = pentry.get()
        cnx = pymysql.connect(host='localhost', user=username, password=password, db='universityhealthservices')

        cur = cnx.cursor()
        cur.callproc('selectHCforP', entry,)

        rows = cur.fetchall()
        # get column names
        col = [d[0] for d in cur.description]

        # Print result set of selectHCforP()
        for row in rows:
            for name, val in zip(col, row):
                selecthclabel = tk.Label(text=f"{name}: {val}")
                selecthclabel.pack()
        cnx.commit()
    elif entry4 == "appointments":
        username = uentry.get()
        password = pentry.get()
        cnx = pymysql.connect(host='localhost', user=username, password=password, db='universityhealthservices')

        cur = cnx.cursor()
        cur.callproc('selectAptforP', entry, )

        rows = cur.fetchall()
        # get column names
        col = [d[0] for d in cur.description]

        # Print result set of selectAptforP()
        for row in rows:
            for name, val in zip(col, row):
                result = cur.fetchall()
                if result is None:
                    selecthclabel = tk.Label(text='You have no appointments on record.')
                    selecthclabel.pack()
                else:
                    selecthclabel = tk.Label(text=f"{name}: {val}")
                    selecthclabel.pack()
        cnx.commit()
    elif entry4 == "bills":
        username = uentry.get()
        password = pentry.get()
        cnx = pymysql.connect(host='localhost', user=username, password=password, db='universityhealthservices')

        cur = cnx.cursor()
        cur.callproc('selectBillforP', entry, )

        rows = cur.fetchall()
        # get column names
        col = [d[0] for d in cur.description]

        # Print result set of selectBillforP()
        for row in rows:
            for name, val in zip(col, row):
                result = cur.fetchall()
                if result is None:
                    selecthclabel = tk.Label(text='You have no bills on record.')
                    selecthclabel.pack()
                else:
                    selecthclabel = tk.Label(text= f"{name}: {val}")
                    selecthclabel.pack()
        cnx.commit()
    else:
        label4 = tk.Label(text='Invalid attribute. Please try again. Start by entering the patient id ')
        label4.pack()
        entry5 = tk.Entry(width=50)
        entry5.pack()
        sudtryagainbutton = tk.Button(text="Try again", command=lambda: check_patid(entry5.get()))
        sudtryagainbutton.pack()
        

window = tk.Tk()
window.title("UHSD")

initiallabel = tk.Label(text='Welcome to University Health Services! \n Please input your username.')
initiallabel.pack()

uentry = tk.Entry(fg='black', bg='white', width=50)
uentry.pack()

initiallabel2 = tk.Label(text='Please input your password.')
initiallabel2.pack()

pentry = tk.Entry(fg='black', bg='white', width=50)
pentry.pack()

label = tk.Label(text='Please input your patient id')
label.pack()

entry = tk.Entry(fg='black', bg='white', width=50)
entry.pack()

button = tk.Button(text="Login", command= check_login)
button.pack()

patid = entry.get()

window.mainloop()

