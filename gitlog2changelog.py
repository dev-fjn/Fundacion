#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2008 Marcus D. Hanwell <marcus@cryos.org>
# Distributed under the terms of the GNU General Public License v2 or later
#
# https://github.com/cryos/avogadro/blob/master/scripts/gitlog2changelog.py

import string
import re
import os

# Execute git log with the desired command line options.

fin = os.popen('git log --summary --stat --no-merges --date=short', 'r')

# Create a ChangeLog file in the current directory.

fout = open('ChangeLog', 'w')

# Set up the loop variables in order to locate the blocks we want

authorFound = False
dateFound = False
messageFound = False
filesFound = False
message = ''
messageNL = False
files = ''
prevAuthorLine = ''

# The main part of the loop

for line in fin:

    # The commit line marks the start of a new commit object.

    if string.find(line, 'commit') >= 0:

        # Start all over again...

        authorFound = False
        dateFound = False
        messageFound = False
        messageNL = False
        message = ''
        filesFound = False
        files = ''
        continue
    elif re.match('Author:', line) >= 0:

    # Match the author line and extract the part we want

        authorList = re.split(': ', line, 1)
        author = authorList[1]
        author = author[0:len(author) - 1]
        authorFound = True
    elif re.match('Date:', line) >= 0:

    # Match the date line

        dateList = re.split(':   ', line, 1)
        date = dateList[1]
        date = date[0:len(date) - 1]
        dateFound = True
    elif re.match('    git-svn-id:', line) >= 0:

    # The svn-id lines are ignored

        continue
    elif re.search('Signed-off-by', line) >= 0:

    # The sign off line is ignored too

        continue
    elif authorFound & dateFound & messageFound == False:

    # Extract the actual commit message for this commit
        # Find the commit message if we can

        if len(line) == 1:
            if messageNL:
                messageFound = True
            else:
                messageNL = True
        elif len(line) == 4:
            messageFound = True
        else:
            if len(message) == 0:
                message = message + line.strip()
            else:
                message = message + ' ' + line.strip()
    elif re.search('files changed', line) >= 0:

    # If this line is hit all of the files have been stored for this commit

        filesFound = True
        continue
    elif authorFound & dateFound & messageFound:

    # Collect the files for this commit. FIXME: Still need to add +/- to files

        fileList = re.split(' \| ', line, 2)
        if len(fileList) > 1:
            if len(files) > 0:
                files = files + ', ' + fileList[0].strip()
            else:
                files = fileList[0].strip()

    # All of the parts of the commit have been found - write out the entry

    if authorFound & dateFound & messageFound & filesFound:

        # First the author line, only outputted if it is the first for that
        # author on this day

        authorLine = date + '  ' + author
        if len(prevAuthorLine) == 0:
            fout.write(authorLine + '\n')
        elif authorLine == prevAuthorLine:
            pass
        else:
            fout.write('\n' + authorLine + '\n')

        # Assemble the actual commit message line(s) and limit the line length
        # to 80 characters.

        commitLine = '* ' + files + ': ' + message
        i = 0
        commit = ''
        while i < len(commitLine):
            if len(commitLine) < i + 78:
                commit = commit + '\n  ' + commitLine[i:len(commitLine)]
                break
            index = commitLine.rfind(' ', i, i + 78)
            if index > i:
                commit = commit + '\n  ' + commitLine[i:index]
                i = index + 1
            else:
                commit = commit + '\n  ' + commitLine[i:78]
                i = i + 79

        # Write out the commit line

        fout.write(commit + '\n')

        # Now reset all the variables ready for a new commit block.

        authorFound = False
        dateFound = False
        messageFound = False
        messageNL = False
        message = ''
        filesFound = False
        files = ''
        prevAuthorLine = authorLine

# Close the input and output lines now that we are finished.

fin.close()
fout.close()
