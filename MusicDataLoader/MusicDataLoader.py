import re
import os.path

# ___________________________________________________________________________________________#
# Program Name:     Music Data Loader                                                       #
# Description:      Create a parser for Wayne Cripps .tab file format and create various    #
#                   attributes to be run in a Machine Learning classifier                   #
# Project Title:    Estimating the difficulty of guitar music                               #
# Author:   Fergus Cutting                                                                  #
# Advisor:  Gavin Cawley                                                                    #
# 3rd Year Project for CMP, University of East Anglia                                       #
# ___________________________________________________________________________________________#
print("________________________________________________________________")
print("|--------------------Music Data Loader V1.0---------------------|")
print("|----------For use alongside Tab Difficulty Estimator-----------|")
print("|------Designed by Fergus Cutting for his 3rd year project------|")
print("________________________________________________________________")


def parse_file(music_file):
    begin = False
    tempoChange = 0
    tempoChangePerBar = 0
    tempoDifficulty = 0
    barSize = 0
    barTempo = 0
    lastTempo = 0
    tempoList = []
    diffTempoList = []
    lineCount = 0
    bars = -1
    chordWidthTotal = 0
    chordLengthTotal = 0
    chordTotal = 0
    chordWidthAve = 0
    chordLengthAve = 0
    noteDensity = 0
    totalChar = 0

    # Checks for bars and piece beginning
    for line in music_file:
        chord = []
        noSlash = False
        if line[0] == "b":
            begin = True
        if not begin:
            continue
        lineCount = lineCount + 1

        # Fingering input removal
        while not noSlash:
            try:
                line.index("\\")
            except ValueError:
                noSlash = True
            else:
                line = line[0: line.index("\\"):] + line[line.index("\\") + 2::]

        # Remove non supported characters from line
        line = re.sub(r'[^a-zA-Z0-9 ]', '', line)
        tempLine = re.sub(' ', '', line)
        totalChar = totalChar + len(tempLine)

        # Tempo handler for first whitelisted character in a line
        if len(line) > 0:
            if line[0] == "b":

                count = 0
                for i in tempoList:
                    tempoDifficulty = tempoDifficulty + int(i)
                    count += count
                for tempo in tempoList:
                    if tempo not in diffTempoList:
                        diffTempoList.append(tempo)
                for temp in range(len(diffTempoList)):
                    if temp != 0:
                        if diffTempoList[temp] != diffTempoList[temp - 1]:
                            tempoChange = tempoChange + 1
                    else:
                        if diffTempoList[temp] != lastTempo:
                            tempoChange = tempoChange + 1
                    temp += temp
                tempoChangePerBar = tempoChangePerBar + tempoChange
                tempoChange = 0
                barSize = 0
                barTempo = 0
                diffTempoList = []
                tempoList = []
                bars = bars + 1

            elif line[0].isdecimal():
                barTempo = barTempo + int(line[0])
                barSize += barSize
                tempoList.append(line[0])
                lastTempo = int(line[0])

            elif line[0] == "x":
                barTempo = barTempo + lastTempo
                barSize += barSize
                tempoList.append(lastTempo)

            # ---------------------Chord Calculations begin--------------------------
            # removes tempo identifier from line
            line = line[1:]
            for character in line:
                if character.isalnum() or len(chord) > 0:
                    if character.isalpha():
                        character = str(ord(character) - 97)
                    # adds note to current chord
                    chord.append(character)
                # Removes unfretted notes from edge of arrays
                if len(chord) - 1 == 0:
                    while chord[-1] == 0:
                        chord.pop()
                if len(chord) > 1:
                    chordWidth = len(chord)
                    # Removes 0 and blankspace characters to add arra
                    tempChord = [i for i in chord if i != "0"]
                    tempChord = [int(i) for i in tempChord if i != " "]
                    # Calculates average length of a chord
                    if len(tempChord) > 0:
                        chordLength = (max(tempChord) - min(tempChord) + 1)
                    else:
                        chordLength = 1

                    chordLengthTotal = chordLengthTotal + chordLength
                    chordWidthTotal = chordWidthTotal + chordWidth
                    chordTotal = chordTotal + 1
    music_file.close()

    # Calculate various attributes based on file details
    if lineCount != 0 and bars != 0 and chordTotal != 0:
        tempoChangePerBar = tempoChangePerBar / bars
        tempoDifficulty = tempoDifficulty / lineCount
        chordLengthAve = chordLengthTotal / chordTotal
        chordWidthAve = chordWidthTotal / chordTotal
        noteDensity = totalChar / bars

        print("Final tempo difficulty: ", tempoDifficulty)
        print("Average number of tempo changes per bar: ", tempoChangePerBar)
        print("Average chord len/width is: ", chordLengthAve, " ", chordWidthAve)
        print("Note Density is ", noteDensity)

    # Write the class and attributes to MusicData.csv
    MusicData.write(
        str(grade) + "," + str(tempoDifficulty) + "," + str(tempoChangePerBar) + "," + str(
            chordLengthAve) + ","
        + str(chordWidthAve) + "," + str(noteDensity) + "\n")
    print("Added file with grade: ", grade, " and attributes", str(tempoDifficulty),
          str(tempoChangePerBar),
          str(chordLengthAve), str(chordWidthAve), noteDensity)
    MusicData.close()


cont = False
valid = False
abspath = os.path.abspath(__file__)
dir_name = os.path.dirname(abspath)

while not valid:
    folder = input("input folder? (y/n) - note: all must be the same grade")

    # Folder input
    if folder == "y":
        valid = True
        while not cont:
            # Folder validation
            folderName = input("Copy Path of folder:")
            folderName = folderName.strip('"')
            dirName = os.fsencode(folderName)
            if os.path.exists(dirName):
                for fileInput in os.listdir(dirName):
                    fileInput = os.fsdecode(fileInput)
                    if fileInput.endswith(".tab"):
                        while not cont:
                            # Grade validation
                            grade = input("Please Enter grade of pieces in folder: (1-8)")
                            if grade.isdigit():
                                grade = int(grade)
                                if 0 < grade < 9:
                                    grade = str(grade)
                                    cont = True
                            else:
                                print("Must be integer 1-8")
                        music_path = os.path.join(dir_name, 'MusicData.csv')
                        MusicData = open(
                            music_path, "a")
                        file = open(folderName + '\\' + fileInput, 'r')
                        parse_file(file)
            else:
                print("Folder not found")

    # Individual file input
    elif folder == "n":
        valid = True
        while not cont:
            fileInput = input("Please Enter full path of the .tab file to add to dataset")
            fileInput = fileInput.strip('"')
            if os.path.exists(fileInput):
                file = open(fileInput, "r")
                while not cont:
                    grade = input("Please Enter grade of new piece: (1-8)")
                    if grade.isdigit():
                        grade = int(grade)
                        if 0 < grade < 9:
                            grade = str(grade)
                            cont = True
                    else:
                        print("Must be integer 1-8")
                music_path = os.path.join(dir_name, 'MusicData.csv')
                MusicData = open(music_path, "a")
                parse_file(file)
            else:
                print("File not Found")
    else:
        print("please enter y or n")
