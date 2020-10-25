#! /usr/bin/env python
__author__ = 'Arana Fireheart'

""" Write tags to file
Usage:
    tagfile.py "TagName" FileName1 FileName2 

    You can use wildcards for the file name. Use quotes if spaces in tags.
    To check if it worked, use xattr -l FileName
"""

import sys
import subprocess
from os.path import expanduser

def writeXattrs(fileName, tagList):
    """ writexattrs(F,TagList):
    writes the list of tags to three xattr fields on a file-by file basis:
    "kMDItemFinderComment","_kMDItemUserTags","kMDItemOMUserTags
    Uses subprocess instead of xattr module. Slower but no dependencies"""

    result = ""

    plistFront = '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0"><array>'
    plistEnd = '</array></plist>'
    plistTagString = ''
    for tag in tagList:
        plistTagString = plistTagString + '<string>{}</string>'.format(tag.replace("'","-"))
    tagText = plistFront + plistTagString + plistEnd

    OptionalTag = "com.apple.metadata:"
    xattrList = ["kMDItemFinderComment","_kMDItemUserTags","kMDItemOMUserTags"]
    for Field in xattrList:
        xattrCommand = 'xattr -w {0} \'{1}\' "{2}"'.format(OptionalTag + Field, tagText.encode("utf8"), fileName)
        if DEBUG:
            sys.stderr.write("XATTR: {}\n".format(xattrCommand))
        procString = subprocess.check_output(xattrCommand, stderr=subprocess.STDOUT,shell=True)
        result += procString
    return result


DEBUG = False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
    else:
        tagList = [sys.argv[1]]
        # print TagList
        # Or you can hardwire your tags here
        # TagList = ['Orange','Green']
        fileList = sys.argv[2:]
        for index in range(0, len(fileList)):
            if '~' in fileList[index]:
                homeDirectory = expanduser("~")
                fileList[index] = fileList[index].replace('~', homeDirectory)


        for fileName in fileList:
            writeXattrs(fileName, tagList)