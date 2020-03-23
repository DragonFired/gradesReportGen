#! /usr/bin/env python
__author__ = 'Arana Fireheart'

from subprocess import check_output, STDOUT
from os import scandir, path
from datetime import datetime
from os.path import expanduser

home = expanduser("~")
startingFolder = "Dropbox/PineManor/CSC101/Fall18"
# startingFolder = "Dropbox/Newbury/CS106/Fall 17"
startingFolder = path.join(home, startingFolder)
gradeFileName = "gradeReportData.txt"
gradeOutputFile = "gradeReportFinal2.tab"
# from xattr import listxattr
gradesList = []

gradeConversion = {"Red": 0, "Yellow": 75, "Green":100}
currentStudent = currentAssignment = ""
with open(path.join(startingFolder, gradeFileName), 'r') as masterGradeFile:
    for line in masterGradeFile.readlines():
        currentContent = line.strip().split(' ')
        if currentContent[0] == "Student" and currentContent[1] != currentStudent:
            currentStudent = currentContent[1][:-1]                 # Found new student record
            currentAssignment = currentContent[3][:-1]
        elif currentContent[0] == "Program:":
            try:
                gradesList.append((currentStudent, currentAssignment, currentContent[1], gradeConversion[currentContent[3]]))
            except KeyError:
                print("{0} not a gradable color".format(currentContent[3]))
with open(path.join(startingFolder, gradeOutputFile), 'w') as outputFile:
    for name, assignment, file, grade in gradesList:
        outputFile.write("{0}\t{1}\t{2}\t{3}\n".format(name, assignment, file, grade))