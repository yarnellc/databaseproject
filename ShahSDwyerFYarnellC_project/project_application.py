#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 18:56:41 2023

@authors: faithdwyer chloeyarnell
"""

import flask
import mysql.connector
import pymysql
import sys
import traceback

# PROMPT USER
username = input('Enter MySQL username: ')
password = input('Enter MySQL password: ')
# check if login is valid, stop if invalid
try:
    cnx = pymysql.connect(host='localhost', user=username, password=password, db='universityhealthservices')
    cnx.close()
except pymysql.err.OperationalError as e:
    print('Error: %d: %s' % (e.args[0], e.args[1]))
    traceback.print_exc()

# MAIN MENU
cur = None  # establish cursor outside of loop
while True:
    response = input(
        'Welcome to University Health Services! Please select one of the following options: \n'
        'university, health center, staff, patients, insurance, bills, appointment, exams, diagnosis, '
        'treatment, or exit? \n')

    #### PATIENTS RESPONSE ####
    if response == 'patients':
        # establish connection
        try:
            cnx = pymysql.connect(host='localhost', user=username, password=password,
                                  db='universityhealthservices')
    
            # start cursor for idNum from patients
            cur = cnx.cursor()
            cur.execute('SELECT idNum FROM Patients')
            rows = cur.fetchall()  # store the tuples
            cnx.close()
    
            # initialize an empty list to store the idNums
            patient_info = []
            for (idNum,) in rows:
                patient_info.append(idNum)
    
            # if idNum in list, ask to select update or delete
            while True:
                idNum = (input('idNum: '))
                if int(idNum) in patient_info:
                    option = input('Would you like to select, update, or delete that id? ')
                    if option == 'select':
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        cur.callproc('selectPat', (int(idNum),))
    
                        rows = cur.fetchall()
                        # get column names
                        col = [d[0] for d in cur.description]
    
                        # Print result set of selectPat()
                        for row in rows:
                            for name, val in zip(col, row):
                                print(f"{name}: {val}")
                 
                        cnx.commit()
                        break
                    
                    elif option == 'delete':
                        patientId = idNum
                        firstName = input('Enter first name: ')
                        lastName = input('Enter last name: ')
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        # call deletePat procedure
                        cur.callproc('deletePatient', (patientId, firstName, lastName))
                        print('This patients data has been deleted! This includes their patient profile, '
                              'medical history, and insurance information!')
                        cnx.commit()
                        cnx.close()
    
                        break
                    elif option == 'update':
                        while True:
                            # establish connection
                            cnx = pymysql.connect(host='localhost', user=username, password=password,
                                                  db='universityhealthservices')
                            cur = cnx.cursor()
                            value = input(
                                'Enter the attribute you would like to update (first name, last name, college, '
                                'phone number, professor (0/1), student (0/1), TA (0/1), last treatment): \n')
                            list_attributes = ['first name', 'last name', 'college', 'phone number', 'professor',
                                               'student', 'TA', 'last treatment']
                            # ask user what attribute they want to update
                            if value in list_attributes:
                                if value == 'college':
                                    new_college = input('Enter the name of the new college: ')
                                    cur.execute("SELECT name FROM University WHERE name = %s", (new_college,))
                                    result = cur.fetchone()
                                    if result is None:
                                        answer = input('This college does not exist in our database. If you would like '
                                                       'to add this college, please enter add college. '
                                                       'If not, please enter retry: ')
                                        if answer == 'retry':
                                            continue
                                        if answer == 'add college':
                                            break
                                new_value = input(f'Enter the updated {value}: ')
                                cur.callproc('updatePat', (int(idNum), value, new_value))
                                print('This attribute has been updated!')
                                cnx.commit()
                                cnx.close()
                                break
                            # if the attribute doesn't exist, prompt to try again
                            else:
                                print("That attribute is incorrect. Please check your spelling and try again.")
                    break
                # if not in list, ask if they want to create or retry
                else:
                    option = input(
                        'That idNum does not exist in our system. If want to add a  patient respond yes. '
                        'If not respond no: ')
                    if option == 'yes':
                        idNum = int(input('Please re-enter the idNum you would like to create: '))
                        firstName = input('Enter first name: ')
                        lastName = input('Enter last name: ')
                        college = input('Enter college: ')
                        phoneNum = input('Enter phone number: ')
                        Professor = int(input('Is the patient a professor? (0/1): '))
                        Student = int(input('Is the patient a student? (0/1): '))
                        TA = int(input('Is the patient a TA? (0/1): '))
                        last_treatment = input('When was the last date of treatment?')
                        print("Please provide this patients medical history: ")
                        patient = idNum
                        
                        conditions = input("Please indicate any past medical conditions this patient has: ")
                        allergies = input("Please indicate any allergies this patient has: ")
                        surgeries = input("Please indicate past surgeries this patient has had: ")
                        immunizations = input("Please enter up to date information on immunizations: ")
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()                        
                        # check if  college  in the Patients table
                        cur.execute("SELECT name FROM University WHERE name = %s", (college,))
                        result = cur.fetchone()
                        # if not, do not let user add patient
                        if result is None:
                            answer = input("Invalid patient college. If you would like to add this college to our "
                                           "database, please enter add college. \n"
                                           "If you would like to try again with a valid college please enter retry: ")
                            if answer == "retry":
                                continue
                            elif answer == "add college":
                                break
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        # call insertPat
                        cur.callproc('insertPatient', (idNum, firstName, lastName, college, phoneNum, Professor,
                                                       Student, TA, last_treatment, patient,
                                                       conditions, allergies, surgeries, immunizations))
                        cnx.commit()
                        print("We have added that id to our system!")
                        break
                    # if they don't want to add this patient, prompt to retry
                    if option == "no":
                        print("Please enter a valid idNum.")
    
            # reprompt user for for a general error
        except pymysql.Error:
            print('Error, try again: ', str(pymysql.Error))
            traceback.print_exc()
    
        #### EXAMS RESPONSE ####
    elif response == "exams":
        try:
            # establish connection
            cnx = pymysql.connect(host='localhost', user=username, password=password,
                                  db='universityhealthservices')
    
            # start cursor for select examnum from exam
            cur = cnx.cursor()
            cur.execute('SELECT examNum FROM Exam')
            rows = cur.fetchall()  # store the tuples
            cnx.close()
    
            # initialize an empty list to store exam nums in
            exam_info = []
            for (examNum,) in rows:
                exam_info.append(examNum)
    
            # if the exam num is in the list show the exam vals
            while True:
                examNum = int(input('Please input examNum: '))
                if int(examNum) in exam_info:
                    option = input(
                        "Would you like to select exam information, delete this exam, or update exam information. "
                        "Please enter select or update. ")
                    if option == "select":
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        cur.callproc('selectExam', (int(examNum),))
    
                        rows = cur.fetchall()
                        col = [d[0] for d in cur.description]
    
                        # Print result set of selectExam()
                        for row in rows:
                            for name, val in zip(col, row):
                                print(f"{name}: {val}")
                        cnx.commit()
                        break
                    
                    elif option == 'delete':
                        examNum = examNum
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        # call deleteExam procedure
                        cur.callproc('deleteExam', (examNum,))
                        print('This exam has been deleted!')
                        cnx.commit()
                        cnx.close()
    
                        break     
                    
                    elif option == "update":
                        while True:
                            # establish connection
                            cnx = pymysql.connect(host='localhost', user=username, password=password,
                                                  db='universityhealthservices')
                            cur = cnx.cursor()
                            value = input(
                                'Enter the attribute you would like to update '
                                '(room number, patient id, staff id, date): ')
                            list_attributes = ['room number', 'patient id', 'staff id', 'date']
                            # if value is in list, prompt to update
                            if value in list_attributes:
                                if value == 'staff id':
                                    new_staff = input('Please enter the new staff id: ')
                                    cur.execute("SELECT staffId FROM Staff WHERE staffId = %s", (new_staff,))
                                    result = cur.fetchone()
                                    if result is None:
                                        answer = input("Invalid staffid. If you would like to add this staff member, "
                                                       "enter add staff. If you would like to retry, enter retry: ")
                                        if answer == "retry":
                                            continue
                                        elif answer == "add staff":
                                            break
                                if value == "patient id":
                                    new_pat = input("Please enter the patient id: ")
                                    cur.execute("SELECT idNum FROM Patients WHERE idNum = %s", (new_pat,))
                                    result = cur.fetchone()
                                    if result is None:
                                        answer = input("This patient does not exist in our database. "
                                                       "If you would like to add this patient, enter add patient. "
                                                       "If you would like to retry, enter retry: ")
                                        if answer == "retry":
                                            continue
                                        elif answer == "add patient":
                                            break
                                new_value = input(f'Enter the updated {value}: ')
                                cur.callproc('updateExam', (int(examNum), value, new_value))
                                print(f'The {value} has been updated! ')
                                cnx.commit()
                                cnx.close()
                                break
                            # if attribute is not in list, prompt to retry
                            else:
                                print("That attribute is incorrect. Please check your spelling and try again.")
    
                    break

                # if not, prompt to add exam
                else:
                    option = input(
                        'This exam does not exist in our system. '
                        'Would you like to create a new exam? If so, type create if not, type no. \n'
                        'Please note the system will generate its own examNum for you: ')
                if option == 'create':
                    while True:
                        # get user input
                        roomNum = int(input('Insert a room number: '))
                        patient = int(input('Insert the patient\'s idNum: '))
                        staff = int(input('Insert the staff ID of the staff on this case: '))
                        date = (input('Insert the date of this exam (YYYY-MM-DD): '))
                        apt = int(input('Insert the aptNum that involves this exam: '))
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        # check if patient and appointment exist and are correctly associated in the Apppointment table
                        cur.execute("SELECT aptNum FROM Appointment "
                                    "WHERE aptNum = %s AND Appointment.patient = %s", (apt, patient))
                        result = cur.fetchone()
                        # if patient and exam are not in Appointment table, don't let the user add this exam
                        if result is None:
                            answer = input("Invalid patient idNum or aptNum. "
                                           "If you would like to add this patient or this appointment to our database, "
                                           "please enter add patient or appointment. \n"
                                           "If you would like to try again with a valid id please enter retry: ")
                            if answer == "retry":
                                continue
                            elif answer == "add patient" \
                                    or answer == "add appointment" \
                                    or answer == "add patient or appointment":
                                break  # redirect to main menu
                        else:
                            # check if staff is in the Staff table
                            cur.execute("SELECT staffId FROM Staff WHERE staffId = %s", (staff,))
                            s_result = cur.fetchone()
                            # if staff not in staff table, don't let user add exam
                            if s_result is None:
                                print("Invalid staff ID. Please try again.")
                            else:
                                # if both exist, create
                                cur.callproc('insertExam', (roomNum, patient, staff, date, apt))
                                cnx.commit()
                                print("A new exam has been inserted!")
                                break
                    break
                else:
                    print('invalid exam number, please try again.')

        # reprompt user for for a general error
        except pymysql.Error:
            print('Error, try again: ', str(pymysql.Error))
            traceback.print_exc()
    
    #### INSURANCE RESPONSE ####
    elif response == "insurance":
        try:
            cnx = pymysql.connect(host='localhost', user=username, password=password,
                                  db='universityhealthservices')
    
            # start cursor for select patient from healthinsurance
            cur = cnx.cursor()
            cur.execute('SELECT patient FROM healthInsurance')
            rows = cur.fetchall()  # store the tuples in patient variable
            cnx.close()
    
            # initialize an empty list to store idNums in health insurance
            insur_info = []
            for (patient,) in rows:
                insur_info.append(patient)
    
            # if the patient is in the list show the insurance results
            while True:
                patient = int(input('Please input patient id: '))
                if int(patient) in insur_info:
                    option = input(
                        "Would you like to select this patients information or update their information. "
                        "Please enter select or update. ")
                    if option == "select":
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        # call on procedure
                        cur.callproc('selectInsur', (int(patient),))
                        # get rows and column names
                        rows = cur.fetchall()
                        col = [d[0] for d in cur.description]
    
                        # Print result set of selectPat()
                        for row in rows:
                            for name, val in zip(col, row):
                                print(f"{name}: {val}")
                        cnx.commit()
                        break
                    
                    elif option == "update":
                        while True:
                            # establish connection
                            cnx = pymysql.connect(host='localhost', user=username, password=password,
                                                  db='universityhealthservices')
                            cur = cnx.cursor()
                            value = input('Enter the attribute you would like to update '
                                          '(provider, policyNum, or copay): ')
                            list_attributes = ['provider', 'policyNum', 'copay']
                            # if value is in list of attributes, allow to update
                            if value in list_attributes:
                                new_value = input(f'Enter the updated {value}: ')
                                cur.callproc('updateInsur', (int(patient), value, new_value))
                                print(f'The {value} has been updated! ')
                                cnx.commit()
                                cnx.close()
                                break
                            # else, reprompt
                            else:
                                print("That attribute is incorrect. Please check your spelling and try again.")

                    break
                else:
                    option = input(
                        'This patient does not have insurance information on file. '
                        'Would you like to add it? If so, type create if not, type no: ')
                    if option == 'create':
                        # get user input
                        provider = (input('Please enter the name of the provider: '))
                        patient = int(input('Please enter the patient id number: '))
                        policyNum = int(input('Please enter the policy number: '))
                        copay = int(input("Please enter the copay for this provider: "))
                        # establish a connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        # check if patient is in the Patients table
                        cur.execute("SELECT idNum FROM Patients WHERE idNum = %s", (patient,))
                        result = cur.fetchone()
                        # if in patients table, allow to insert
                        if result is not None:
                            cur.callproc('insertInsur', (provider, patient, policyNum, copay))
                            cnx.commit()
                            print("A new policy has been added to our system!")
                            break
                        # else, reprompt
                        else:
                            answer = input("This patient doesn't exist in our database. "
                                           "To re enter a valid id respond retry. \n"
                                           "If you would like to add this patient to our database, "
                                           "respond add patient: ")
                            if answer == "retry":
                                continue
                            elif answer == "add patient":
                                break
                    
                    else:
                        print('invalid exam number, please try again.')

        # reprompt user for for a general error
        except pymysql.Error:
            print('Error, try again: ', str(pymysql.Error))
            traceback.print_exc()
    
        #### BILLS RESPONSE ####
    elif response == "bills":
        # establish connection
        try:
            cnx = pymysql.connect(host='localhost', user=username, password=password,
                                  db='universityhealthservices')
    
            # start cursor for select billnum from Bills
            cur = cnx.cursor()
            cur.execute('SELECT billNum FROM Bills')
            rows = cur.fetchall()  # store the tuples in billing variable
            cnx.close()
    
            # initialize an empty list to store bill nums in
            bill_info = []
            for (billNum,) in rows:
                bill_info.append(billNum)
    
            # if the bill num is in the list, ask if they would like to select or update
            while True:
                billNum = int(input('Please input the billNum: '))
                if int(billNum) in bill_info:
                    option = input(
                        "Would you like to select bill information or update bill information. "
                        "Please enter select or update. ")
                    if option == "select":
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        # call on procedure
                        cur.callproc('selectBill', (int(billNum),))
                        # get rows and column names
                        rows = cur.fetchall()
                        col = [d[0] for d in cur.description]
    
                        # Print result set of selectBill()
                        for row in rows:
                            for name, val in zip(col, row):
                                print(f"{name}: {val}")
                        cnx.commit()
                        break
                    elif option == "update":
                        while True:
                            # establish connection
                            cnx = pymysql.connect(host='localhost', user=username, password=password,
                                                  db='universityhealthservices')
                            cur = cnx.cursor()
                            # ask user what attribute they want to update
                            value = input(
                                'Enter the attribute you would like to update '
                                '(amount due, payment status, payment date): ')
                            list_attributes = ['amount due', 'payment status', 'payment date']
                            # if value is in list of attributes, allow to update
                            if value in list_attributes:
                                new_value = input(f'Enter the updated {value}: ')
                                cur.callproc('updateBill', (int(billNum), value, new_value))
                                print(f'The {value} has been updated! ')
                                cnx.commit()
                                cnx.close()
                                break
                            # if not, reprompt
                            else:
                                print("That attribute is incorrect. Please check your spelling and try again.")
                    break
    
                # if bill not in list, ask if they want to add the bill
                else:
                    option = input(
                        'This bill does not exist. Would you like to create a new bill? '
                        'If so, type create if not, type no: ')
                    if option == 'create':
                        # get user input
                        patient = int(input('Insert the patient\'s idNum: '))
                        billNum = billNum
                        amountDue = int(input('Insert the amount due for this bill: '))
                        paymentStatus = bool(input('Insert whether or not this bill has been paid (0/1): '))
                        exam = int(input('Insert the examNum for this bill: '))
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        # check if  patient is in the Patients table
                        cur.execute("SELECT idNum FROM Patients WHERE idNum = %s", (patient,))
                        result_b = cur.fetchone()
                        # if not, either retry or add patient
                        if result_b is None:
                            answer = input("Invalid patient idNum. "
                                           "If you would like to add this patient to our database, "
                                           "please enter add patient. \n"
                                           "If you would like to try again with a valid id please enter retry: ")
                            if answer == "retry":
                                continue
                            elif answer == "add patient":
                                break
                        # check if exam and patient are correctly associated in the Exam table
                        cur.execute("SELECT examNum FROM Exam "
                                    "WHERE examNum = %s AND Exam.patient = %s", (exam, patient))
                        result_b = cur.fetchone()
                        # if not, either retry or add patient
                        if result_b is None:
                            answer = input(
                                "Invalid examNum. "
                                "If you would like to add or update this exam, please enter add exam. \n"
                                "If you would like to try again with a valid examNum please enter retry: ")
                            if answer == "retry":
                                continue
                            elif answer == "add exam":
                                break
                        # if both patient and exam are valid, allow insert and call insertBill
                        cur.callproc('insertBill', (patient, billNum, amountDue, paymentStatus, exam))
                        cnx.commit()
                        print("A new bill has been created! ")
                        break
                    # Prompt to retry
                    else:
                        print('Invalid bill number, please try again.')

        # reprompt user for for a general error
        except pymysql.Error:
            print('Error, try again: ', str(pymysql.Error))
            traceback.print_exc()

    #### EXIT RESPONSE ####
    elif response == 'exit':
        print('You have closed this program!')
        break

    #### TREATMENT RESPONSE ####
    elif response == 'treatment':
        try:
            cnx = pymysql.connect(host='localhost', user=username, password=password,
                                  db='universityhealthservices')
    
            # start cursor for select treatmentNum from treatment
            cur = cnx.cursor()
            cur.execute('SELECT treatmentNum FROM treatment')
            rows = cur.fetchall()
            cnx.close()
    
            # initialize an empty list to store treatment nums in
            treat_info = []
            for (treatmentNum,) in rows:
                treat_info.append(treatmentNum)
    
            # if the bill num is in the list show the treatment vals
            while True:
                treatmentNum = int(input('Please input the treatNum: '))
                if int(treatmentNum) in treat_info:
                    option = input(
                        "Would you like to select, or delete treatment information. "
                        "Please enter select, update or delete. ")
                    if option == "select":   
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        # call procedure
                        cur.callproc('selectTreat', (int(treatmentNum),))
    
                        rows = cur.fetchall()
                        col = [d[0] for d in cur.description]
    
                        # Print result set of selectTreat()
                        for row in rows:
                            for name, val in zip(col, row):
                                print(f"{name}: {val}")
                        cnx.commit()
                        break
                    
                    elif option == 'delete':
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        cur.callproc('deleteTreat', (treatmentNum,))
                        print('This treatment has been deleted!')
                        cnx.commit()
                        cnx.close()
    
                        break
                   
                else:
                    option = input(
                        'This treatment does not exist. Would you like to create a new treatment? '
                        'If so, type create if not, type no: ')
                    if option == 'create':
                        # get user input
                        treatmentNum = treatmentNum
                        diagnosis = int(input('Insert the diagnosis number: '))
                        date = (input('Insert the date of treatment (YYYY-MM-DD): '))
                        patient = int(input('Insert the patient idNum: '))
                        type1 = input("Enter the treatment type (Shot, PrescriptionMeds, OTCMeds, Referral, or None): ")
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        # check if  patient  in the Patients table
                        cur.execute("SELECT idNum FROM Patients WHERE idNum = %s", (patient,))
                        result = cur.fetchone()
                        # if not, do not let user add treatment
                        if result is None:
                            answer = input("Invalid patient idNum. "
                                           "If you would like to add this patient to our database, "
                                           "please enter add patient. \n"
                                           "If you would like to try again with a valid id please enter retry: ")
                            if answer == "retry":
                                continue
                            elif answer == "add patient":
                                break
                        # check if the diagnosis is in diagnosis table with the associated patient
                        cur.execute("SELECT diagNum FROM Diagnosis "
                                    "WHERE diagNum = %s AND patient = %s", (diagnosis, patient))
                        result_e = cur.fetchone()
                        # if not, don't let user add treatment
                        if result_e is None:
                            answer = input("Invalid diagNum. If you would like to add this diagnosis to our database, "
                                           "please enter add diagnosis. \n"
                                           "If you would like to try again with a valid idiagNum please enter retry: ")
                            if answer == "retry":
                                continue
                            elif answer == "add diagnosis":
                                break
                        # if both diagnosis and patient are valid, call procedure
                        cur.callproc('insertTreat', (treatmentNum, diagnosis, date, patient, type1))
                        cnx.commit()
                        print("A new treatment has been created! ")
                        break
                    else:
                        print('invalid treatment number, please try again.')
                     
        except pymysql.Error:
            print('Error, try again: ', str(pymysql.Error))
            traceback.print_exc()

    #### DIAGNOSIS RESPONSE ####
    elif response == 'diagnosis':
        try:
            cnx = pymysql.connect(host='localhost', user=username, password=password,
                                  db='universityhealthservices')
    
            # start cursor for select diagNum from Diagnosis
            cur = cnx.cursor()
            cur.execute('SELECT diagNum FROM diagnosis')
            rows = cur.fetchall()
            cnx.close()
    
            # initialize an empty list to store diagNums in
            diag_info = []
            for (diagNum,) in rows:
                diag_info.append(diagNum)
    
            # if the bill num is in the list show the diagnosis vals
            while True:
                diagNum = int(input('Please input the diagNum: '))
                if int(diagNum) in diag_info:
                    option = input(
                        "Would you like to select, delete or update diagnosis information. "
                        "Please enter select, update or delete. ")
                    if option == "select":   
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        cur.callproc('selectDiag', (int(diagNum),))
                        # get rows and col names
                        rows = cur.fetchall()
                        col = [d[0] for d in cur.description]
    
                        # Print result set of selectDiag()
                        for row in rows:
                            for name, val in zip(col, row):
                                print(f"{name}: {val}")
                        cnx.commit()
                        break
                    
                    elif option == 'delete':
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        diagNum = diagNum
                        cur = cnx.cursor()
                        # call deleteDiag
                        cur.callproc('deleteDiag', (diagNum,))
                        print('This diagnosis has been deleted!')
                        cnx.commit()
                        cnx.close()
                    break
                else:
                    option = input(
                        'This diagnosis does not exist. Would you like to create a new diagnosis? '
                        'If so, type create if not, type no: ')
                    if option == 'create':
                        # get user input
                        diagNum = diagNum
                        description = (input('Insert the description: '))
                        illness = bool(input('Insert whether or not the patient has an illness that will be lasting '
                                             '(0/1): '))
                        exam = int(input('Insert the exam Num: '))
                        patient = int(input("Enter the patient idNum: "))
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        # check if  patient  in the Patients table
                        cur.execute("SELECT idNum FROM Patients WHERE idNum = %s", (patient,))
                        result = cur.fetchone()
                        # if not, do not let user add diagnosis
                        if result is None:
                            answer = input("Invalid patient idNum. "
                                           "If you would like to add this patient to our database, "
                                           "please enter add patient. \n"
                                           "If you would like to try again with a valid id please enter retry: ")
                            if answer == "retry":
                                continue
                            elif answer == "add patient":
                                break
                        # check if the exam and patient are correctly associated
                        cur.execute("SELECT examNum FROM Exam WHERE examNum = %s AND patient = %s", (exam, patient))
                        result_e = cur.fetchone()
                        # if not, do not let user add diagnosis
                        if result_e is None:
                            answer = input("Invalid  examNum. If you would like to add this exam to our database, "
                                           "please enter add exam. \n"
                                           "If you would like to try again with a valid examNum please enter retry: ")
                            if answer == "retry":
                                continue
                            elif answer == "add exam":
                                break
                        # if both exam and patient are valid, call procedure and insert diagnosis
                        cur.callproc('insertDiag', (diagNum, description, illness, exam, patient))
                        cnx.commit()
                        print("A new diagnosis has been created! ")
                        break
                    else:
                        print('invalid diagNum, please try again.')

        except pymysql.Error:
            print('Error, try again: ', str(pymysql.Error))
            traceback.print_exc()

    #### STAFF RESPONSE ####
    elif response == 'staff':
        # establish connection
        try:
            cnx = pymysql.connect(host='localhost', user=username, password=password,
                                  db='universityhealthservices')

            # start cursor for select staffId from Staff
            cur = cnx.cursor()
            cur.execute('SELECT staffId FROM Staff')
            rows = cur.fetchall()  # store the tuples
            cnx.close()

            # initialize an empty list to store staff IDs in
            staff_info = []
            for (staffId,) in rows:
                staff_info.append(staffId)

            # if the staff ID is in the list, ask to select, delete, or update
            while True:
                staffId = int(input('Please input the staff Id: '))
                if int(staffId) in staff_info:
                    option = input(
                        "Would you like to select, delete or update staff information? "
                        "Please enter select, update or delete. ")
                    if option == "select":
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        cur.callproc('selectStaff', (int(staffId),))

                        rows = cur.fetchall()
                        # get column names
                        col = [d[0] for d in cur.description]

                        # Print result set of selectStaff()
                        for row in rows:
                            for name, val in zip(col, row):
                                print(f"{name}: {val}")
                        cnx.commit()
                        break
                    elif option == 'delete':
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        staffId = int(input('Please input the staff Id you would like to delete: '))
                        cur = cnx.cursor()
                        # call deleteStaff procedure
                        cur.callproc('deleteStaff', (staffId,))
                        print('This staff member has been deleted!')
                        cnx.commit()
                        cnx.close()

                        break

                    elif option == "update":
                        while True:
                            # establish connection
                            cnx = pymysql.connect(host='localhost', user=username, password=password,
                                                  db='universityhealthservices')
                            cur = cnx.cursor()
                            # ask user what attribute they want to update
                            value = input(
                                'Enter the attribute you would like to update (first name, last name, role): ')
                            list_attributes = ['first name', 'last name', 'role']
                            if value in list_attributes:
                                new_value = input(f'Enter the updated {value}: ')
                                cur.callproc('updateStaff', (int(staffId), value, new_value))
                                print(f'The {value} has been updated! ')
                                cnx.commit()
                                cnx.close()
                                break
                            # if attribute doesn't exist, prompt to try again
                            else:
                                print("That attribute is incorrect. Please check your spelling and try again.")

                    break
                # if not in list, ask if they want to create or retry
                else:
                    option = input(
                        'This staff member does not exist. Would you like to create a new staff member?'
                        'If so, type create if not, type no: ')
                    if option == 'create':

                        staffId = staffId
                        firstName = (input('Insert their first name: '))
                        lastName = (input('Insert their last name: '))
                        healthCenter = (input('Insert the name of the health center that they work at: '))
                        role = input("Enter what position they will work as "
                                     "(OfficeAssistant, Manager, Technician, Nurse, or MD): ")
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        
                        # check if the health center exists
                        cur.execute("SELECT name FROM HealthCenter WHERE name = %s", (healthCenter,))
                        result_hc = cur.fetchone()
                        # if not, do not let user add staff member
                        if result_hc is None:
                            answer = input("Invalid health center. "
                                           "If you would like to add this center to our database, "
                                           "please enter add center. \nIf you would like to try again "
                                           "with a valid health center, please enter retry: ")
                            if answer == "retry":
                                continue
                            elif answer == "add center":
                                break
                        # call insertStaff
                        cur.callproc('insertStaff', (staffId, firstName, lastName, healthCenter, role))
                        cnx.commit()
                        print("A new staff member has been added! ")
                        break
                    # if they don't want to add this member, prompt to retry
                    else:
                        print('Please enter a valid staff id.')

        # reprompt user for general error
        except pymysql.Error:
            print('Error, try again: ', str(pymysql.Error))
            traceback.print_exc()

    #### APPOINTMENT RESPONSE ####
    elif response == 'appointment':
        try:
            # establish connection
            cnx = pymysql.connect(host='localhost', user=username, password=password,
                                  db='universityhealthservices')

            # start cursor for select patient from appointment
            cur = cnx.cursor()
            cur.execute('SELECT patient FROM Appointment')
            rows = cur.fetchall()
            cnx.close()

            # initialize an empty list to store patients with appointments in
            apt_info = []
            for (patient,) in rows:
                apt_info.append(patient)

            while True:
                patient = int(input('Please input the patient Id: '))
                if int(patient) in apt_info:
                    option = input(
                        "Would you like to select, delete or update this appointment information? "
                        "Please enter select, update or delete. ")
                    if option == "select":
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        cur.callproc('selectApt', (int(patient),))

                        rows = cur.fetchall()
                        col = [d[0] for d in cur.description]

                        # Print result set of selectApt()
                        for row in rows:
                            for name, val in zip(col, row):
                                print(f"{name}: {val}")
                        cnx.commit()
                        break
                    
                    elif option == 'delete':
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        # get user input
                        patient = int(input('Please input the patient Id whose appointment you would like to delete: '))
                        cur = cnx.cursor()
                        cur.callproc('deleteApt', (patient,))
                        print('This appointment has been deleted!')
                        cnx.commit()
                        cnx.close()

                        break

                    elif option == "update":
                        while True:
                            # establish connection
                            cnx = pymysql.connect(host='localhost', user=username, password=password,
                                                  db='universityhealthservices')
                            cur = cnx.cursor()
                            value = input(
                                'Enter the attribute you would like to update (date, time, reason, exam): ')
                            list_attributes = ['date', 'time', 'reason', 'exam']
                            # check that attribute entered is valid
                            if value in list_attributes:
                                if value == 'exam':
                                    new_exam = input('Enter the examNum of the new exam: ')
                                    cur.execute("SELECT examNum FROM Exam "
                                                "WHERE examNum = %s AND patient = %s", (new_exam, patient,))
                                    result = cur.fetchone()
                                    if result is None:
                                        answer = input('This exam is not associated with the patient '
                                                       'for this appointment. \nIf you would like to add or update this'
                                                       ' exam, please enter add or update exam. '
                                                       'If not, please enter retry: \n')
                                        if answer == 'retry':
                                            continue
                                        if answer == "add exam" \
                                                or answer == "update exam" \
                                                or answer == "add or update exam":
                                            break
                                new_value = input(f'Enter the updated {value}: ')
                                # if yes, call procedure
                                cur.callproc('updateApt', (patient, value, new_value))
                                print(f'The {value} has been updated! ')
                                cnx.commit()
                                cnx.close()
                                break
                            # if not, reprompt
                            else:
                                print("That attribute is incorrect. Please check your spelling and try again.")

                    break
                else:
                    option = input(
                        'This patient does not have an appointment. '
                        'Would you like to create an appointment for them? \n'
                        'If so, type create if not, type no: ')
                    if option == 'create':
                        # get user input
                        patient = patient
                        date = (input('Insert the appointment date (YYYY-MM-DD): '))
                        time = (input('Insert the appointment time (HH:MM:SS): '))
                        reason = (input('Insert the patients reason for scheduling this appointment: '))
                        # establish connection
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        # check if patient is in the Patients table
                        cur.execute("SELECT idNum FROM Patients WHERE idNum = %s", (patient,))
                        result = cur.fetchone()
                        # if patient is not in patients table, don't let the user add this exam
                        if result is None:
                            answer = input("Invalid patient idNum. "
                                           "If you would like to add this patient to our database, "
                                           "please enter add patient. \n"
                                           "If you would like to try again with a valid id please enter retry: ")
                            if answer == "retry":
                                continue
                            elif answer == "add patient":
                                break  # redirect to main menu
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()

                        cur.callproc('insertApt1', (patient, date, time, reason))
                        cnx.commit()
                        print("A new appointment  has been added! ")
                        break
                    else:
                        print('invalid patient id, please enter a valid id if you would like to add an appointment.')

        except pymysql.Error:
            print('Error, try again: ', str(pymysql.Error))
            traceback.print_exc()

    #### HEALTH CENTER RESPONSE ####
    elif response == 'health center':
        # establish connection
        try:
            cnx = pymysql.connect(host='localhost', user=username, password=password,
                                  db='universityhealthservices')

            # start cursor for select name from health center
            cur = cnx.cursor()
            cur.execute('SELECT name FROM healthCenter')
            rows = cur.fetchall()  # store the tuples
            cnx.close()

            # initialize an empty list to store health center names in
            hc_info = []
            for (name,) in rows:
                hc_info.append(name)

            # if the name is in the list, ask to select, insert, or delete hc
            while True:
                name = input('Please input the name of the health center: ')
                if name in hc_info:
                    option = input(
                        "Would you like to select, insert, or delete health center information? "
                        "Please enter select, insert, or delete. ")
                    if option == "select":
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        cur.callproc('selectHC', (name,))

                        rows = cur.fetchall()
                        # get column names
                        col = [d[0] for d in cur.description]

                        # Print result set of selectHC() 
                        for row in rows:
                            for name, val in zip(col, row):
                                print(f"{name}: {val}")
                        cnx.commit()
                        break

                    elif option == 'delete':
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        name = name
                        cur = cnx.cursor()
                        # call deleteHC procedure
                        cur.callproc('deleteHC', (name,))
                        print('This health center has been deleted!')
                        cnx.commit()
                        cnx.close()

                        break
                # if not in list, ask if they want to create or retry
                else:
                    option = input(
                        'This health center does not exist. Would you like to create a health center? '
                        'If so, type create if not, type no: ')
                    if option == 'create':
                        name = name
                        stName = (input('Insert the street name of this health center\'s address: '))
                        stNum = input('Insert the street number of this health center\'s address: ')
                        zip = int(input('Insert the zip code this health center is in: '))
                        state = input("Enter the state this health center is in (two letter abbreviation): ")
                        city = input("Enter the city this health center is in: ")
                        university = input("Enter the name of the university that this center is part of: ")
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        # check if university is in the University table
                        cur.execute("SELECT name FROM University WHERE name = %s", (university,))
                        result = cur.fetchone()
                        # if not, do not let user add health center
                        if result is None:
                            answer = input(
                                "Invalid university. If you would like to add this university to our database, "
                                "please enter add university. \n"
                                "If you would like to try again with a valid university please enter retry: ")
                            # if they don't want to add the health center,
                            if answer == "retry":
                                continue
                            elif answer == "add university":
                                break
                        # call insertHC
                        cur.callproc('insertHC', (name, stNum, stName, zip, state, city, university))
                        cnx.commit()
                        print("A new health center has been created! ")
                        break
                    else:
                        print('invalid health center, please try again.')

        # reprompt user for general error
        except pymysql.Error:
            print('Error, try again: ', str(pymysql.Error))
            traceback.print_exc()

    #### UNIVERSITY RESPONSE ####
    elif response == "university":
        try:
            # establish connection
            cnx = pymysql.connect(host='localhost', user=username, password=password,
                                  db='universityhealthservices')

            # start cursor for name from university
            cur = cnx.cursor()
            cur.execute('SELECT name FROM University')
            rows = cur.fetchall()  # store the tuples
            cnx.close()

            # initialize an empty list to store university names in
            u_info = []
            for (name,) in rows:
                u_info.append(name)

            # if the university name is in the list, ask to select update or delete
            while True:
                name1 = input('Please input the university name: ')
                if name1 in u_info:
                    option = input(
                        "Would you like to select or delete university information? Please enter select or delete. ")
                    if option == "select":
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        cur.callproc('selectU', (name1,))
                        rows = cur.fetchall()
                        # get column names
                        col = [d[0] for d in cur.description]

                        # Print result set of selectU()
                        for row in rows:
                            for name, val in zip(col, row):
                                print(f"{name}: {val}")
                        cnx.commit()
                        break
                    elif option == "delete":
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        name = input('Please input the university name you would like to delete: ')
                        cur = cnx.cursor()
                        # call deleteU procedure
                        cur.callproc('deleteU', (name,))
                        print('This university has been deleted!')
                        cnx.commit()
                        cnx.close()

                    break

                # if university name not in list, ask if they want to add it
                else:
                    option = input(
                        'This university does not exist. Would you like to create a university? '
                        'If so, type create if not, type no: ')
                    if option == 'create':
                        name = name1
                        stName = (input('Insert the street name of this health center\'s address: '))
                        stNum = input('Insert the street number of this health center\'s address: ')
                        zip = int(input('Insert the zip code this health center is in: '))
                        state = input("Enter the state this health center is in (two letter abbreviation): ")
                        city = input("Enter the city this health center is in: ")
                        # establish connection
                        cnx = pymysql.connect(host='localhost', user=username, password=password,
                                              db='universityhealthservices')
                        cur = cnx.cursor()
                        # call insertU
                        cur.callproc('insertU', (name1, stNum, stName, zip, state, city))
                        cnx.commit()
                        print("We have added that university to our system!")
                        break
                    if option == "no":
                        print("Please enter a valid university")

        # reprompt user for general error
        except pymysql.Error:
            print('Error, try again: ', str(pymysql.Error))
            traceback.print_exc()


