#!/usr/bin/env python

"""
    This script can parse CSV databases.

    To use it, you should call getInfo(teamName) function.
    It returns the list with following structure:
        [TeamName, OpponentTeamName, TeamNameScore, OpponentTeamNameScore, isTeamHome].
    If team played the match at the home stadium, it returns True, otherwise - False.
"""

import os
import csv

dir = "..\\datasets"
teamName = ""
teamsStat = []

def getInfo(teamName):
    if teamName == "":
        teamName = "Arsenal"
    takeCSV(teamName)

def takeCSV(teamName):
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):
            if name.endswith("csv"):
                parseCSV(path, teamName)
        else:
            takeCSV(dir)

def parseCSV(path, teamName):
    inputFile = open(path, "rb")
    rdr = csv.reader(inputFile)
    for rec in rdr:
        try:
            isTeamHome = rec[2] == teamName
            isTeamAway = rec[3] == teamName
            if isTeamHome:
                teamsStat.append([rec[2],rec[3],rec[4],rec[5],isTeamHome])
            elif isTeamAway:
                teamsStat.append([rec[3],rec[2],rec[5],rec[4],isTeamHome])
         except:
             pass
    inputFile.close()

if __name__ == '__main__':
    getInfo(teamName)
    for team in teamsStat:
        print team
