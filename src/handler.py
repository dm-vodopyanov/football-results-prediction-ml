import numpy as np
import os
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn import metrics

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

		score_1 = int(params[4])
		score_2 = int(params[5])
		goals_1 = int(params[2])
		goals_2 = int(params[3])

		minScore = min(score_1, score_2)
		maxScore = max(score_1, score_2)
		selfField = False
		if params[6] == "True\n":
			selfField = True
		else:
			selfField = False

		game_x.append(minScore)
		game_x.append(maxScore)
		if score_1 != minScore:
			tmp = goals_1
			goals_1 = goals_2
			goals_2 = tmp
			selfField = not selfField
		
		if selfField:
			game_x.append(1)
		else:
			game_x.append(0)

		if goals_1 > goals_2:
			game_y = 2
		elif goals_1 < goals_2:
			game_y = 0
		else:
			game_y = 1

		X_batch.append(game_x)
		Y_batch.append(game_y)

def selectNonRepeatingData(X_list, Y_list, X_set, Y_set):
	y_delete_indexes = [] 
	for i in range(0, len(X_list), 1):
		elem = X_list[i];
		if elem not in X_set:
			X_set.append(elem)
		else:
			y_delete_indexes.append(i)
	
	for i in range(0, len(Y_list), 1):
		if i not in y_delete_indexes:
			Y_set.append(Y_list[i])

# method actions

def naiveBayes(train_X, train_Y, test_X):
	X = train_X[:]
	Y = train_Y[:]
	X_test = test_X[:]
	model_NB = MultinomialNB(alpha=0.0)
	model_NB.fit(X, Y)
	predictedNB = model_NB.predict(X_test)
	return predictedNB

def svmachine(train_X, train_Y, test_X):
	X = train_X[:]
	Y = train_Y[:]
	X_test = test_X[:]
	clf = svm.SVC()
	clf.fit(X, Y)
	predictedSVM = clf.predict(X_test)
	return predictedSVM

def randomForest(train_X, train_Y, test_X):
	X = train_X[:]
	Y = train_Y[:]
	X_test = test_X[:]
	forest = RandomForestClassifier(10)
	forest.fit(X, Y)
	predictedRF = forest.predict(X_test)
	return predictedRF

def methodResults(predictedY, correctY):
	rightCount = 0
	for i in range (0, len(correctY), 1):
		if predictedY[i] == correctY[i]:
			rightCount = rightCount + 1

	percent = (float(rightCount) / len(test_batch_Y)) * 100
	print "  Percent: ", percent

if __name__ == '__main__':
	start_path = "..\\txt"
	start_path = "D:\\MachineLearning\\football-results-prediction-ml\\txt"

	teams_files = getFilesData(start_path)

	X_list = []
	Y_list = []
	test_batch_X = []
	test_batch_Y = []

	allGamesCount = 0
	for team_file in teams_files:
		team_games = team_file.readlines()
		#prepare train_batch
		getBatch(team_games, 0, len(team_games) - 4, X_list, Y_list)
		#prepare test_batch
		getBatch(team_games, len(team_games) - 4, len(team_games), test_batch_X, test_batch_Y)
		allGamesCount = allGamesCount + len(team_games)

	X_train_set = []
	Y_train_set = []
	selectNonRepeatingData(X_list, Y_list, X_train_set, Y_train_set)
	X_test_set = []
	Y_test_set = []
	selectNonRepeatingData(test_batch_X, test_batch_Y, X_test_set, Y_test_set)

	#creating np data
	X_train_np = np.array(X_train_set)
	Y_train_np = np.array(Y_train_set)
	X_test_np = np.array(X_test_set)
	Y_test_np = np.array(Y_test_set)

	print "--------------------------------------"
	print "Predicting outcome of football matches"
	print "--------------------------------------"
	print "Number of games from datasets: ", len(X_train_set)
	print "Number of test games:          ", len(X_test_set)
	print ""

	predNB = naiveBayes(X_train_np, Y_train_np, X_test_np)
	print "Results of Naive Bayes:"
	methodResults(predNB, Y_test_np)
	#print(metrics.classification_report(Y_test_np, predNB))

	predRF = randomForest(X_train_np, Y_train_np, X_test_np)
	print "Results of Random Forest:"
	methodResults(predRF, Y_test_np)
	#print(metrics.classification_report(Y_test_np, predNB))

	predSVM = svmachine(X_train_np, Y_train_np, X_test_np)
	print "Results of Support Vectors Machine:"
	methodResults(predSVM, Y_test_np)
	#print(metrics.classification_report(Y_test_np, predNB))