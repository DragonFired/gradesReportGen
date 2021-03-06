#! /usr/bin/env python
__author__ = 'Arana Fireheart'

from subprocess import check_output, STDOUT
from os import scandir, path, walk
from datetime import datetime
from os.path import expanduser
from tablib import Dataset
#
# This program 'looks' at files in the given directory for labels.
# If a RED, GREEN or YELLOW label are found, it adds that file to a grade report
# file generated for each assignment directory found in each student's directory.
#

home = expanduser("~")
startingFolder = "Dropbox/SNHU/CS114/Spring20"
startingFolder = path.join(home, startingFolder)
gradeFileName = "gradeReport.txt"
gradeDataFilename = "gradeReportData.txt"
gradeConversion = {"Red": 0, "Yellow": 75, "Green": 100, "Purple": 120}
fileEndingsByLanguage = {"Python": (".py",), "C++": (".cpp", ".h",)}
languageChoice = "C++"

masterList = ""
dataList = ""
spreadsheet = Dataset(headers=["Name", "Assignment", "filename", "Grade", "Numeric Grade"])

todaysDateTime = datetime.now().ctime().replace(" ", "_")

def saveXlsxFile(dataSetName, filename):
    with open(filename, 'wb') as spreadsheetFile:
        spreadsheetFile.write(dataSetName.export('xlsx'))

def getStudentList(folderName):
    namesList = []
    for directoryItem in scandir(folderName):
        if directoryItem.is_dir():
            if not directoryItem.name.startswith('.'):
                namesList.append(directoryItem.name)
    return namesList

if path.exists(startingFolder):
    studentList = getStudentList(startingFolder)
    row = 2

    for student in studentList:
        studentName = student.split('-')[0]
        for assignmentDirectory in scandir(path.join(startingFolder, student)):
            assignmentsList = []
            if assignmentDirectory.is_dir():
                noTagsFound = True
                codeFilesFound = False
                for rootPath, dirs, files in walk(path.join(startingFolder, student, assignmentDirectory)):
                    for file in files:
                        # noFilesFound = False
                        fullFilePath = path.join(rootPath, file)
                        command = 'tag "' + fullFilePath + '"'
                        returnString = check_output(command, stderr=STDOUT, shell=True).decode(
                            "UTF8")
                        filename, fileExtention = path.splitext(fullFilePath)
                        if fileExtention in fileEndingsByLanguage[languageChoice]:
                            codeFilesFound = True
                        if returnString.count('\t') >= 1:
                            (fileName, tags) = returnString.split('\t')
                            assignmentsList.append((path.basename(fileName), tags.strip()))
                if len(assignmentsList) > 0:
                    fileContents = "Student {0}: Assignment {1}:\n".format(student, assignmentDirectory.name)
                    for item in assignmentsList:
                        fileContents += ("Program: {0} Grade: {1}\n".format(item[0], item[1]))
                        dataList += "{0}\t{1}\t{2}\t{3}\n".format(studentName,assignmentDirectory.name, item[0], gradeConversion[item[1]])
                        calculationText = f'=IF(D{row}="Green",100,IF(D{row}="Yellow",75,IF(D{row}="Red",0,"-")))'
                        spreadsheet.append((studentName, assignmentDirectory.name, item[0], item[1], calculationText))
                        row += 1
                elif noTagsFound and codeFilesFound:
                    fileContents = "Student {0}: Assignment {1}:\n".format(student, assignmentDirectory.name)
                    fileContents += "Assignments not graded yet."
                    calculationText = f'=IF(D{row}="Green",100,IF(D{row}="Yellow",75,IF(D{row}="Red",0,"-")))'
                    spreadsheet.append((studentName, assignmentDirectory.name, item[0], "None Yet", calculationText))
                    row += 1
                else:
                    fileContents = "Student {0}: Assignment {1}:\n".format(student, assignmentDirectory.name)
                    fileContents += "No assignments to grade"
                    calculationText = f'=IF(D{row}="Green",100,IF(D{row}="Yellow",75,IF(D{row}="Red",0,"-")))'
                    spreadsheet.append((studentName, assignmentDirectory.name, item[0], "Missing", calculationText))
                    row += 1
                fileContents += "\nRecorded on: {0}\n".format(todaysDateTime)
                with open(path.join(startingFolder, student, assignmentDirectory, gradeFileName), 'w') as gradeFile:
                    gradeFile.write(fileContents)
                    masterList += fileContents + '\n\n'

    saveXlsxFile(spreadsheet, path.join(startingFolder, "allGrades.xlsx"))
    with open(path.join(startingFolder, gradeFileName) , 'a') as masterGradeFile:
        masterGradeFile.write(50 * '-' + '\n\n')
        masterGradeFile.write(masterList)

    with open(path.join(startingFolder, gradeDataFilename) , 'w') as masterDataFile:
        masterDataFile.write(dataList)
else:
    print("Folder {0} doesn't exist".format(startingFolder))