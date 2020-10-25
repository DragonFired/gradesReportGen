#! /usr/bin/env python
__author__ = 'Arana Fireheart'

from datetime import datetime
from os.path import expanduser, join


class GradeMaximumExceededError(Exception):
    pass


def generateAssignmentGrade(studentGradesDictionary, assignmentName, maxGrade=100):
    try:
        studentGradesDictionary[assignmentName] = assignmentTotal / assignmentCounts[assignmentName]
    except ZeroDivisionError:
        studentGradesDictionary[assignmentName] = 0
    if studentGradesDictionary[assignmentName] > maxGrade:
        raise GradeMaximumExceededError


def getGradesData(filename):
    namesList = []
    dataList = []
    print("Reading grades from file {0}".format(filename))
    with open(filename, 'r') as gradesInputFile:
        for inputLine in gradesInputFile.readlines():
            dataList.append(inputLine.strip())
            name, assignment, filename, grade = inputLine.split('\t')
            if name not in namesList:
                namesList.append(name)
        dataList.sort()
    return namesList, dataList


if __name__ == "__main__":
    home = expanduser("~")
    startingFolder = "Dropbox/SNHU/CS110/Fall2019"
    startingFolder = join(home, startingFolder)
    gradeDataFilename = "gradeReportData.txt"
    gradesSummaryFilename = "gradesByStudent.txt"
    gradesImportableFilename = "gradesByStudentImportable.txt"
    fullAssignmentList = ["Conditionals", "Dictionaries", "Files", "FinalProject", "Functions", "Loops",
                          "LoopsContitionalsLists", "Reading1", "Reading2", "Strings", "Variables&Data"]
    assignmentList = ["Conditionals", "Functions", "LoopsContitionalsLists", "Reading1", "Strings", "Variables&Data"]
    assignmentCounts = {"Conditionals": 3,
                        "Dictionaries": 2,
                        "Files": 0,
                        "Functions": 3,
                        "Loops": 5,
                        "LoopsContitionalsLists": 10,
                        "Reading1": 16,
                        "Reading2": 0,
                        "Strings": 4,
                        "Variables&Data": 5,
                        "FinalProject": 0,
                        }

    todaysDateTime = datetime.now().ctime().replace(" ", "_")
    gradeDataFilename = join(startingFolder, gradeDataFilename)

    try:
        studentList, fullDataList = getGradesData(gradeDataFilename)

        gradesData = {}
        previousName = ""
        for line in fullDataList:
            name, assignment, filename, grade = line.split('\t')
            if name != previousName:
                if previousName != "":
                    gradesData[previousName] = studentsGrades
                    try:
                        generateAssignmentGrade(studentsGrades, previousAssignment)
                    except GradeMaximumExceededError:
                        print("Grade for student {0} was over 100".format(previousName))
                studentsGrades = {}   # Beginning of student's data group
                previousName = name
                previousAssignment = assignment
                assignmentTotal = float(grade)
            else:
                if previousAssignment == assignment:
                    assignmentTotal += float(grade)
                else:
                    try:
                        generateAssignmentGrade(studentsGrades, previousAssignment)
                    except GradeMaximumExceededError:
                        print("Grade for student {0} was over 100".format(previousName))
                    previousAssignment = assignment
                    assignmentTotal = float(grade)
        # Complete dealing with the last student and assignment in the list
        try:
            generateAssignmentGrade(studentsGrades, previousAssignment)
        except GradeMaximumExceededError:
            print("Grade for student {0} was over 100".format(previousName))
        gradesData[name] = studentsGrades

        # Output grades to file.
        readableOutputFilename = join(startingFolder, gradesSummaryFilename)
        importableOutputFilename = join(startingFolder, gradesImportableFilename)
        print("Writing readable grades to file {0}".format(readableOutputFilename))
        print("Writing importable grades to file {0}".format(importableOutputFilename))

        with open(readableOutputFilename, 'w') as readableOutputFile, open(importableOutputFilename, 'w') as importableOutputFilename:
            readableOutputFile.write("Date: {0}\n\n".format(todaysDateTime))
            for student in studentList:
                if student in gradesData:
                    currentStudentsGrades = gradesData[student]
                    readableOutputFile.write("Grades for {0}\n".format(student))
                    for assignment in assignmentList:
                        if assignment in currentStudentsGrades:
                            readableOutputFile.write("Assignment: {0}\t Grade: {1:5.2f}\n".format(assignment, currentStudentsGrades[assignment]))
                            importableOutputFilename.write("{0}\t{1}\t{2:5.2f}\n".format(student, assignment, currentStudentsGrades[assignment]/100))
                        else:
                            readableOutputFile.write("Assignment: {0}\t Grade: {1}\n".format(assignment, 0))
                            importableOutputFilename.write("{0}\t{1}\t{2:5.2f}\n".format(student, assignment, 0))
                else:
                    readableOutputFile.write("No grades for {0}\n".format(student))
                readableOutputFile.write('\n')
    except FileNotFoundError:
        print("Folder {0} doesn't exist".format(startingFolder))

