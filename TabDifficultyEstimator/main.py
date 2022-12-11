import pandas as pd
from matplotlib import pyplot as plt
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import plot_confusion_matrix

import random
import re
import os.path
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
# _______________________________________________________________________________________#
# Program name:     Tab Difficulty Estimator                                            #
# Description:      Train a Gaussian Naive Bayes algorithm based on data created in     #
#                   MusicDataLoader.py. Allow the user to test their own file to give   #
#                   an output based on the difficulty of the music                      #
# Project Title:    Estimating the difficulty of guitar music                           #
# Author:   Fergus Cutting                                                              #
# Advisor:  Gavin Cawley                                                                #
# 3rd Year Project for CMP, University of East Anglia                                   #
# _______________________________________________________________________________________#

print("________________________________________________________________")
print("|-----------------Tab Difficulty Estimator V1.0-----------------|")
print("|--------------For use alongside Music Data Loader--------------|")
print("|------Designed by Fergus Cutting for his 3rd year project------|")
print("________________________________________________________________")

diffTempoCount = 0
diffTempoCountPerBar = 0
tempoDifficulty = 0
barSize = 0
barTempo = 0
lastTempo = 0
tempoList = []
diffTempoList = []
grid = False
lineCount = 0
bars = -1
chord = []
chordWidthTotal = 0
chordLengthTotal = 0
chordTotal = 0
chordWidthAve = 0
chordLengthAve = 0
totalChar = 0
noteDensity = 0
grade = 0

# Find absolute path of MusicData.csv folder
abspath = os.path.abspath(__file__)
dir_name = os.path.dirname(abspath)
parent_dir = os.path.dirname(dir_name)
new_path = os.path.join(parent_dir, 'MusicDataLoader')
music_file = os.path.join(new_path, 'MusicData.csv')
music_file = open(music_file, 'r')

music_data = pd.read_csv(music_file, header=None)
# Read in Attributes (X) and classes(y) and store them in pandas Data containers
# X Values: Tempo Difficulty, Number of different note lengths per bar,
#   Average chord length  (largest number of strings between fretted notes),
#   Average chord width (distance between furthest frets)
# Y Values: Grades from 1->8
x = music_data.loc[:, 1:].values
y = music_data.loc[:, 0].values

# Splits the music data into training and testing data to create an accuracy prediction
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30, random_state=random.randrange(1, 999))

gnbAccuracyTest = GaussianNB()
gnb = GaussianNB()

# Trains a Gaussian naive bayes algorithm on the test data
gnbAccuracyTest.fit(x_train, y_train)

GaussianNB(priors=None)
y_pred = gnbAccuracyTest.predict(x_test)
y_train_pred = gnbAccuracyTest.predict(x_train)

accuracy = metrics.accuracy_score(y_test, y_pred)
gnb.fit(x_train, y_train)

plot_confusion_matrix(gnb, x_test, y_test)

cont = False
noSlash = False
begin = False
statistic = False
while not cont:
    statmode = input("Enter statistic mode? This will display a Confusion table and additional statistics (y/n)")
    if statmode == "y":
        statistic = True
        cont = True
    elif statmode == "n":
        statistic = False
        cont = True
    else:
        print("input y/n")
        cont = False
        continue
    while cont:

        fileInput = input("Please Enter full path of the .tab file to classify")
        fileInput = fileInput.strip('"')

        if os.path.exists(fileInput):
            file = open(fileInput, "r")

            for line in file:
                chord = []
                noSlash = False
                grid = False

                # Detects beginning of music
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
                for character in tempLine:
                    totalChar = totalChar + 1

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

                        for item in diffTempoList:
                            diffTempoCount = diffTempoCount + 1

                        diffTempoCountPerBar = diffTempoCountPerBar + diffTempoCount

                        diffTempoCount = 0
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
                            tempChord = [i for i in chord if i != "0"]
                            tempChord = [int(i) for i in tempChord if i != " "]

                            if len(tempChord) > 0:
                                chordLength = (max(tempChord) - min(tempChord) + 1)
                            else:
                                chordLength = 1

                            chordLengthTotal = chordLengthTotal + chordLength
                            chordWidthTotal = chordWidthTotal + chordWidth
                            chordTotal = chordTotal + 1
            file.close()

            # Calculate various attributes based on file details
            if lineCount != 0 and bars != 0 and chordTotal != 0:
                diffTempoCountPerBar = diffTempoCountPerBar / bars
                tempoDifficulty = tempoDifficulty / lineCount
                chordLengthAve = chordLengthTotal / chordTotal
                chordWidthAve = chordWidthTotal / chordTotal
                noteDensity = totalChar / bars

            MusicAttributes = [[tempoDifficulty, diffTempoCountPerBar, chordLengthAve, chordWidthAve, noteDensity]]
            gradePrediction = gnbAccuracyTest.predict(MusicAttributes)
            print("Prediction for this piece is Grade: ", gradePrediction)
            print("Algorithm is running at ", accuracy * 100, "% accuracy")
            cont = True
            music_file.close()
            if statistic:
                precision = 100* metrics.accuracy_score(y_train, y_train_pred)
                recall = 100 * metrics.accuracy_score(y_test, y_pred)
                print("Precision = ", precision)
                print("Recall = " , recall)
                f1 = 2*((recall*precision)/(recall+precision))
                print("F1 value = ", f1)
                plt.show()
        else:
            print("File not Found")
