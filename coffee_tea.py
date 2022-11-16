import math
import operator 
import pandas as pd
import numpy as np

# Импорт из Excel
def getDataFromFile(path):
  dataSet = pd.read_excel(path)
  # Переименовать столбцы
  dataSet = dataSet.rename(columns={
              'имя':'secondName',
              'во сколько встает' : 'wakeUp',
              'средний сон' :'sleepHours',
              'работа' :'employedSet',
              'округ' :'district',
              'что родители' : 'whatParentsDrink',
              'пол' : 'gender',
              'яп' : 'programmingLanguage',
              'пьет' : 'whatTheyDrink',})
  

  dataSet['employedSet'] = dataSet['employedSet']*10
  dataSet['districtSet'] = dataSet.apply(lambda row: 
                        0 if row['district'] == 'ЗАО'
                          else (1 if row['district'] == 'СЗАО'
                          else (2 if row['district'] == 'САО'
                          else (3 if row['district'] == 'СВАО'
                          else (5 if row['district'] == 'ВАО'
                          else (6 if row['district'] == 'ЮВАО'
                          else (7 if row['district'] == 'ЮАО'
                          else (8 if row['district'] == 'ЮЗАО'
                          else (9 if row['district'] == 'ЦАО' 
                          else 10)
                          )))))))
                       , axis=1)
  dataSet['whatParentsDrinkSet'] = dataSet.apply(lambda row: 
                       5 if row['whatParentsDrink'] == 'кофе'
                         else (10 if row['whatParentsDrink'] == 'чай' 
                         else 0) 
                       , axis=1)
  dataSet['genderSet'] = dataSet.apply(lambda row: 
                        5 if row['gender'] == 'мужской'
                          else (10 if row['gender'] == 'женский' 
                          else 0) 
                       , axis=1)
  dataSet['programmingLanguageSet'] = dataSet.apply(lambda row: 
                        0 if row['programmingLanguage'] == 'питон'
                           else (1 if row['programmingLanguage'] == 'свифт'
                           else (2 if row['programmingLanguage'] == 'котлин'
                           else (3 if row['programmingLanguage'] == 'джава'
                           else (4 if row['programmingLanguage'] == 'шарп'
                           else (5 if row['programmingLanguage'] == 'с++'
                           else (6 if row['programmingLanguage'] == 'дс'
                           else (7 if row['programmingLanguage'] == 'луа'
                           else (8 if row['programmingLanguage'] == 'скл' 
                           else 9)
                           )))))))
                       , axis=1)  
  
  return dataSet



# Евклидовое расстояние
def calculateEuclidDistance(row1, row2, length):
	distance = 0

	for x in range(length):
		distance += pow((row1[x] - row2[x]), 2)

	return math.sqrt(distance)

# Наиболее подходящие соседи
def calculateSimilarNeighbors(trainingSet, testRow, k):
	distances = []
	length = len(testRow)-1

	for x in range(len(trainingSet)):
		distance = calculateEuclidDistance(testRow, trainingSet[x], length)
		distances.append((trainingSet[x], distance))

	distances.sort(key=operator.itemgetter(1))
	neighbors = []

	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

def calculateResult(neighbors):
	classCount = {}

	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classCount:
			classCount[response] += 1
		else:
			classCount[response] = 1

	sortedVotes = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]

dataSet = getDataFromFile('dataset3.xlsx')

split = 0.8

trainingSetCount = round(len(dataSet.index) * 0.8)
testSetCount = len(dataSet.index) - trainingSetCount

trainingSet = pd.DataFrame(dataSet,
                  columns=['wakeUp', 'sleepHours', 'employedSet', 'districtSet', 'whatParentsDrinkSet', 'genderSet', 'programmingLanguageSet', 'whatTheyDrink']).head(trainingSetCount)
testSet = pd.DataFrame(dataSet,
                  columns=['wakeUp', 'sleepHours', 'employedSet', 'districtSet', 'whatParentsDrinkSet', 'genderSet', 'programmingLanguageSet', 'whatTheyDrink']).tail(testSetCount)

print ('Train set:')
print (trainingSet)

predictions=[]
k = 3

for x in range(0,len(testSet)):
  neighbors = calculateSimilarNeighbors(trainingSet.to_numpy(), testSet.to_numpy()[x], k)
  result = calculateResult(neighbors)
  predictions.append(result)

testSet = testSet.reset_index()

for x in range(0,len(testSet)):
  testSet.loc[x, 'perdictDrink'] = predictions[x]
print (testSet)