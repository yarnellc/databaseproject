#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 16:52:57 2023

@author: faithdwyer
"""

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

# BILLS
df = pd.read_csv('Bills.csv')

id_nums = df['patient']
amounts_due = df['amountDue']

c = []
status = df['paymentStatus']
for value in status:
    if value == ' TRUE':
        c.append('green')
    else:
        c.append('red')

# Plot the data
plt.bar(id_nums, amounts_due, color = c)
plt.xticks(np.arange(1, 4, 1))
plt.xlabel('idNum')
plt.ylabel('amoundDue')

paid_patch = mpatches.Patch(color='green', label='Paid')
unpaid_patch = mpatches.Patch(color='red', label='Unpaid')
plt.legend(handles=[paid_patch, unpaid_patch])
plt.title('Bills')
plt.savefig('Bills.png')
plt.show()


# PATIENTS

df1 = pd.read_csv('Patients.csv')

count_prof = 0
professor = df1['Professor']
for val in professor:
    if val == ' TRUE':
        count_prof += 1
  
count_stud = 0
stud = df1['Student']
for val in stud:
    if val == ' TRUE':
        count_stud += 1
        
count_TA = 0
TA = df1['TA']
for val in TA:
    if val == ' TRUE':
        count_TA += 1
        
x = ['Professor', 'Student', 'TA']
y = [count_prof, count_stud, count_TA]
plt.bar(x, y)
plt.xlabel('Patient Category')
plt.ylabel('Count')
plt.title('Patient Type')
plt.savefig('PatientType.png')
plt.show()



# TREATMENT
df2 = pd.read_csv('treatment.csv')

types = df2["type"]
counts = types.value_counts()
plt.pie(counts, labels=counts.index, autopct='%1.1f%%')
plt.title('Treatment Types')
plt.savefig('TreatmentTypes.png')
plt.show()


# STAFF
df3 = pd.read_csv('staff.csv')

position = df3['position']
counts = position.value_counts()
plt.pie(counts, labels=counts.index, autopct='%1.1f%%')
plt.title('Staff')
plt.savefig('Staff.png')
plt.show()

# INSURANCE
df4 = pd.read_csv('insurance.csv')
name = df4['provider']
counts = name.value_counts()
plt.pie(counts, labels=counts.index, autopct='%1.1f%%')
plt.title('Insurance')
plt.savefig('Insurance.png')
plt.show()

