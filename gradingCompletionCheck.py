#! /usr/bin/env python
__author__ = 'Arana Fireheart'

from subprocess import check_output, STDOUT
from os import scandir, path, walk
from datetime import datetime
from os.path import expanduser
#
# This program 'looks' at files in the given directory for labels.
# It generates a list of files without a RED, GREEN or YELLOW label.
#

home = expanduser("~")
startingFolder = "Dropbox/SNHU/CS110/Fall2020"
startingFolder = path.join(home, startingFolder)
gradeDataFilename = "ungradedReportData.txt"
gradeConversion = {"Red": 0, "Yellow": 75, "Green": 100, "Purple": 120}
fileEndingsByLanguage = {"Python": (".py",), "C++": (".cpp", ".h",)}
languageChoice = "Python"

masterList = ""
ungradedAssignmentCount = 0
emptyList = ""
emptyAssignmentCount = 0

todaysDateTime = datetime.now().ctime().replace(" ", "_")
masterList += "Recorded on: {0}\n".format(todaysDateTime)

def getStudentList(folderName):
    namesList = []
    for directoryItem in scandir(folderName):
        if directoryItem.is_dir():
            if not directoryItem.name.startswith('.'):
                namesList.append(directoryItem.name)
    return namesList

if path.exists(startingFolder):
    studentList = getStudentList(startingFolder)

    studentList.sort()
    for student in studentList:
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
                        filename, fileExtention = path.splitext(fullFilePath)
                        if fileExtention in fileEndingsByLanguage[languageChoice]:  # File is a code file
                            codeFilesFound = True
                            if returnString.count('\t') == 0:   # It has NOT been tagged.
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

    with open(path.join(startingFolder, gradeDataFilename) , 'w') as masterDataFile:
        masterDataFile.write(masterList)
        masterDataFile.write("\n\n*****************************************\n\nEmpty List:\n")
        masterDataFile.write(emptyList)
    print(f"{ungradedAssignmentCount} ungraded files, and \n{emptyAssignmentCount} empty assignments folders.")
else:
    print("Folder {0} doesn't exist".format(startingFolder))