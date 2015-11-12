import numpy as np
import os
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier

# preparing data

def getFilesData(start_path):
	
	listTeamsData = []
	teams_file_names = os.listdir(start_path)

	for i in range(0, len(teams_file_names), 1):
		listTeamsData.append(open(start_path + "\\" + teams_file_names[i], 'r'))
	return listTeamsData

def getBatch(listParams, start, finish, X_batch, Y_batch):
	for i in range (start, finish, 1):
		game_x = []
		game_y = -1
		params = listParams[i].split(";")
		if params[2] > params[3]:
			game_y = 2
		elif params[2] < params[3]:
			game_y = 0
		else:
			game_y = 1

		game_x.append(int(params[4]))
		game_x.append(int(params[5]))
		if params[6] == "True\n":
			game_x.append(1)
		else:
			game_x.append(0)
		X_batch.append(game_x)
		Y_batch.append(game_y)

# method actions

def naiveBayes(X_data_train, Y_data_train, X_data_test):
	# assigning predictor and target variables
	X = np.array(X_list)
	Y = np.array(Y_list)

	model = MultinomialNB()
	model.fit(X, Y)
	predicted = model.predict(X_data_test)
	return predicted

def randomForest(X_data_train, Y_data_train, X_data_test):
	# assigning predictor and target variables
	X = np.array(X_list)
	Y = np.array(Y_list)

	forest = RandomForestClassifier(100)
	forest = forest.fit(X, Y)
	predicted = forest.predict(X_data_test)
	return predicted

def methodResults(pred, test_batch_Y):
	rightCount = 0
	for i in range (0, len(test_batch_Y), 1):
		if pred[i] == test_batch_Y[i]:
			rightCount = rightCount + 1

	percent = (float(rightCount) / len(test_batch_Y)) * 100
	print "  Percent: ", percent

if __name__ == '__main__':
	start_path = "..\\txt"

	teams_files = getFilesData(start_path)

	X_list = []
	Y_list = []
	test_batch_X = []
	test_batch_Y = []

	for team_file in teams_files:
		team_games = team_file.readlines()
		#prepare train_batch
		getBatch(team_games, 0, len(team_games) - 3, X_list, Y_list)
		#prepare test_batch
		getBatch(team_games, len(team_games) - 3, len(team_games), test_batch_X, test_batch_Y)

	print "--------------------------------------"
	print "Predicting outcome of football matches"
	print "--------------------------------------"
	print "Number of games from datasets: ", len(X_list)
	print "Number of test games:          ", len(test_batch_X)
	print ""

	pred = naiveBayes(X_list, Y_list, test_batch_X)
	print "Results of Naive Bayes:"
	methodResults(pred, test_batch_Y)

	pred = randomForest(X_list, Y_list, test_batch_X)
	print "Results of Random Forest:"
	methodResults(pred, test_batch_Y)
