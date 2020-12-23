#! /usr/bin/env python
__author__ = 'Arana Fireheart'

from subprocess import check_output, STDOUT
from os import scandir, path, walk, stat
from datetime import datetime
from os.path import expanduser
#
# This program 'looks' at files in the given directory for labels.
# It generates a list of files without a RED, GREEN or YELLOW label.
#

monthNames = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
              "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
home = expanduser("~")
startingFolder = "Dropbox/SNHU/CS110/Fall2020"
startingFolder = path.join(home, startingFolder)
gradeDataFilename = "ungradedReportData.txt"
gradeConversion = {"Red": 0, "Yellow": 75, "Green": 100, "Purple": 120}
fileEndingsByLanguage = {"Python": (".py",), "C++": (".cpp", ".h",)}
languageChoice = "Python"


def getLastRecordingDate(filename):
    try:
        with open(filename, 'r') as pastReportFile:
            logLine = pastReportFile.readline()
            dateString = logLine.split(': ')[-1].strip().replace("_", " ")
            lRWeekday, lRMonth, lRDay, lRTime, lRYear = dateString.split()
            lRHour, lRMinute, lRSecond = lRTime.split(':')
            previousDate = datetime(month=monthNames[lRMonth], day=int(lRDay), year=int(lRYear),
                                    hour=int(lRHour), minute=int(lRMinute), second=int(lRSecond))
            return previousDate
    except FileNotFoundError:
        print(f"{filename} doesn't exist.")


def getStudentList(folderName):
    try:
        namesList = []
        for directoryItem in scandir(folderName):
            if directoryItem.is_dir():
                if not directoryItem.name.startswith('.'):
                    namesList.append(directoryItem.name)
        return namesList
    except FileNotFoundError:
        print("Folder {0} doesn't exist".format(folderName))
        exit()


def processStudentFiles(studentNamesList, previousUpdateTime):
    lastUpdated = previousUpdateTime.timestamp()
    masterList = ""
    emptyList = ""
    ungradedAssignmentCount = emptyAssignmentCount = 0

    currentDateTime = datetime.now().ctime().replace(" ", "_")
    masterList += "Recorded on: {0}\n".format(currentDateTime)

    for student in studentNamesList:
        studentName = student.split('-')[0]
        masterList += f"\n{studentName}\n"
        emptyList += f"\n{studentName}\n"
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
                        filename, fileExtension = path.splitext(fullFilePath)
                        if fileExtension in fileEndingsByLanguage[languageChoice]:  # File is a code file
                            codeFilesFound = True
                            fileStats = stat(fullFilePath)
                            lastModTime = fileStats.st_mtime
                            if returnString.count('\t') == 0 or lastModTime > lastUpdated:  # It has NOT been tagged.
                                fileName = returnString
                                if languageChoice == "C++":
                                    projectFoldername = path.split(path.dirname(fileName))[-1]
                                    assignmentsList.append((path.basename(fileName), projectFoldername))
                                else:
                                    assignmentsList.append((path.basename(fileName)))
                if len(assignmentsList) > 0:
                    for item in assignmentsList:
                        fileContents = "Assignment {0}:\tFile: {1}".format(assignmentDirectory.name, item.strip())
                        masterList += fileContents + '\n'
                        ungradedAssignmentCount += 1
                else:
                    emptyList += "Assignment {0}: Empty\n".format(assignmentDirectory.name)
                    emptyAssignmentCount += 1
    return emptyAssignmentCount, emptyList, masterList, ungradedAssignmentCount


def createReportFile(reportFilename):
    with open(reportFilename, 'w') as masterDataFile:
        masterDataFile.write(masterList)
        masterDataFile.write("\n\n*****************************************\n\nEmpty List:\n")
        masterDataFile.write(emptyList)


lastUpdatedDate = getLastRecordingDate(path.join(startingFolder, gradeDataFilename))
studentList = getStudentList(startingFolder)
studentList.sort()
emptyAssignmentCount, emptyList, masterList, ungradedAssignmentCount = processStudentFiles(studentList, lastUpdatedDate)

createReportFile(path.join(startingFolder, gradeDataFilename))
print(f"{ungradedAssignmentCount} ungraded files, and \n{emptyAssignmentCount} empty assignments folders.")
