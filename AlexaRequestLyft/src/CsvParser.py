'''
Created on May 8, 2016

@author: Andrii Usov
'''
import csv
with open('resources/AddressPoint.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    f1=open('../resources/output', 'w+')
    for row in spamreader:
         if len(row) >= 8:
             f1.write(row[1] + " " + row[9] + "\n")
