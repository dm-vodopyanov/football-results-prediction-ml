#!/usr/bin/env python

"""
    This script can parse CSV databases.

    To use it, you should call getInfo(teamName) function.
    It returns the list with following structure:
        [TeamName, OpponentTeamName, TeamNameScore, OpponentTeamNameScore, 
         TeamNameSignificance, OpponentTeamNameSignificanceisTeamNameHome].
    If team played the match at the home stadium, isTeamHome returns True, otherwise - False.
"""

import os
import csv

dir = "..\\datasets"
txtDir = "..\\txt"
teamName = ""
teams = []
teamSignificance = ""
opponentTeamSignificance = ""
teamsStat = []
matchesNumber = 40

def getTeamsNamesList():
    teamsFile = open(dir + "\\allTeams.txt", 'r')
    for team in teamsFile:
        teams.append(team.split(","))
    teamsFile.close();

def getInfo(teams, matchesNumber):
    for team in teams:
        if team[1].endswith("\n"):
            team[1] = team[1][:team[1].find("\n")]
        teamName = team[0]
        teamSignificance = team[1]
        getCSV(teamName, teamSignificance, matchesNumber)
        del teamsStat[:]

def getCSV(teamName, teamSignificance, matchesNumber):
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):
            if name.endswith("csv"):
                parseCSV(path, teamName, teamSignificance, matchesNumber)
        else:
            getCSV(dir)
        saveResults(teamsStat, teamName)

def parseCSV(path, teamName, teamSignificance, matchesNumber):
    inputFile = open(path, "rb")
    rdr = csv.reader(inputFile)
    for rec in rdr: 
        try:
            if (len(teamsStat) <= matchesNumber):
                isTeamHome = rec[2] == teamName
                isTeamAway = rec[3] == teamName
                for team in teams:
                    if isTeamHome:
                        if (team[0] == rec[3]):
                            opponentTeamSignificance = team[1]
                    if isTeamAway:
                        if (team[0] == rec[2]):
                            opponentTeamSignificance = team[1] 
                if opponentTeamSignificance.endswith("\n"):
                    opponentTeamSignificance = opponentTeamSignificance[
                                                            :opponentTeamSignificance.find("\n")]
                if isTeamHome:
                    teamsStat.append([rec[2], rec[3], rec[4], rec[5], 
                                     teamSignificance, opponentTeamSignificance, str(isTeamHome)])
                elif isTeamAway:
                    teamsStat.append([rec[3], rec[2], rec[5], rec[4],
                                     teamSignificance, opponentTeamSignificance, str(isTeamHome)])
        except:
            pass
    inputFile.close()

def saveResults(teamsStat, teamName):
    resFile = open(txtDir + "\\sortedData" + teamName.replace(" ","_") + ".txt", 'w')
    for stat in teamsStat:
        resFile.write(';'.join(stat) + '\n')
    resFile.close()

if __name__ == '__main__':
    getTeamsNamesList()
    getInfo(teams, matchesNumber)
