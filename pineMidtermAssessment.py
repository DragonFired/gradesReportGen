#! /usr/bin/env python
__author__ = 'Arana Fireheart'

from subprocess import check_output, STDOUT
from os import scandir, path, stat
from datetime import datetime
from os.path import expanduser

home = expanduser("~")
# startingFolder = "Dropbox/PineManor/CSC101/Fall18"
startingFolder = "Dropbox/PineManor/CSC101/Fall18"
startingFolder = path.join(home, startingFolder)
gradeFileName = "midtermGradeReport.txt"
writeStudentSummaryFiles = True

masterList = ""
todaysDateTime = datetime.now().ctime().replace(" ", "_")

if path.exists(startingFolder):
    studentFoldersList = []
    studentNameList = []
    for directoryItem in scandir(startingFolder):
        if directoryItem.is_dir():
            if not directoryItem.name.startswith('.'):
                studentFoldersList.append(directoryItem.name)
                studentNameList.append(directoryItem.name[:-9])
else:
    print("Files not found at: {0}".format(startingFolder))
    exit()

masterList += "Recorded on: {0}\n".format(todaysDateTime)
for studentIndex, studentDirectoryName in enumerate(studentFoldersList):
    print('\n' + studentDirectoryName)
    perStudentCount = 0
    with open(path.join(startingFolder, studentDirectoryName, "fileSummary.txt"), 'w') as studentGradeFile:
        for assignmentDirectory in scandir(path.join(startingFolder, studentDirectoryName)):
            if assignmentDirectory.is_dir():
                pythonFileCount = 0
                for file in scandir(path.join(startingFolder, studentDirectoryName, assignmentDirectory)):
                    if file.name.endswith(".py") and stat(path.join(startingFolder, studentDirectoryName, assignmentDirectory, file.name)).st_size != 0:
                        pythonFileCount += 1
                        perStudentCount += 1
                        print('.', end='')
                if writeStudentSummaryFiles:
                    studentGradeFile.writelines("Assignment: {0}: File count: {1}\n".format(assignmentDirectory.name, pythonFileCount))
                masterList += "Student {0}: Assignment {1}: Files: {2}\n".format(studentNameList[studentIndex], assignmentDirectory.name, pythonFileCount)
        masterList += "Student {0}: Total Files: {1}\n\n".format(studentNameList[studentIndex], perStudentCount)
with open(path.join(startingFolder, gradeFileName) , 'w') as masterGradeFile:
    masterGradeFile.write(masterList)